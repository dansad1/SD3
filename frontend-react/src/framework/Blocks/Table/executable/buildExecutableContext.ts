// table/runtime/executable/buildExecutableContext.ts

import type { ExecutableAction } from "./types"

import { resolveRowId } from "./resolveRowId"
import { resolveParams } from "./resolveParams"
import { resolveContextValues } from "./resolveContextValues"
import type { BaseRow } from "../types/runtime"

export function buildExecutableContext<
  T extends BaseRow
>(
  entity: string | undefined,
  row: T,
  action: ExecutableAction
) {
  const rowId = resolveRowId(row)

  const resolvedParams = resolveParams(
    action.params as Record<
      string,
      string | number | boolean | null | undefined
    >,
    row
  )

  const resolvedCtx = resolveContextValues(
    action.ctx as Record<
      string,
      string | number | boolean | null | undefined
    >,
    row
  )

  const baseCtx = {
    ...(entity ? { entity } : {}),
    row,

    ...resolvedCtx,

    id:
      typeof resolvedCtx.id === "string" ||
      typeof resolvedCtx.id === "number"
        ? resolvedCtx.id
        : rowId,
  }

  const finalCtx = {
    ...baseCtx,

    ...resolvedParams,

    id:
      typeof resolvedParams.id === "string" ||
      typeof resolvedParams.id === "number"
        ? resolvedParams.id
        : baseCtx.id,
  }

  console.log("🧾 buildExecutableContext", {
    entity,
    row,
    action,
    rowId,
    resolvedCtx,
    resolvedParams,
    baseCtx,
    finalCtx,
  })

  return {
    rowId,
    finalCtx,
  }
}