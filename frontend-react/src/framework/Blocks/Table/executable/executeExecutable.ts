import { resolveProps } from "@/framework/bind/expression/resolveProps"

import type { ExecutableAction } from "./types"
import { hasStatus } from "./hasStatus"
import { confirmExecutable } from "./confirmExecutable"
import { interpolateTarget } from "./interpolateTarget"
import { buildExecutableContext } from "./buildExecutableContext"
import type { BaseRow } from "../types/runtime"

type Options<T extends BaseRow> = {
  entity?: string
  row: T
  executable: ExecutableAction

  runAction: (
    target: string,
    ctx?: Record<string, unknown>
  ) => Promise<unknown>

  reload?: () => Promise<unknown> | unknown
}

export async function executeExecutable<T extends BaseRow>({
  entity,
  row,
  executable,
  runAction,
  reload,
}: Options<T>) {
  const confirmed = confirmExecutable(executable)

  if (!confirmed) {
    return
  }

  const { finalCtx } = buildExecutableContext(
    entity,
    row,
    executable
  )

  const resolvedPropsCtx = executable.ctx
    ? (resolveProps(executable.ctx, {
        ...finalCtx,
        row,
      }) as Record<string, unknown>)
    : {}

  const resolvedCtx = {
    ...finalCtx,
    ...resolvedPropsCtx,

    id:
      resolvedPropsCtx.id ??
      finalCtx.id ??
      (row as Record<string, unknown>).id ??
      (row as Record<string, unknown>).name,
  }

  console.log("🧾 EXECUTABLE CTX", {
    rawCtx: executable.ctx,
    row,
    finalCtx,
    resolvedPropsCtx,
    resolvedCtx,
  })

  if (executable.to) {
    const resolvedTo = interpolateTarget(
      executable.to,
      resolvedCtx
    )

    if (!resolvedTo) {
      console.warn(
        "executeExecutable: resolvedTo is empty",
        {
          executable,
          resolvedCtx,
          row,
        }
      )
      return
    }

    await runAction(
      resolvedTo,
      resolvedCtx
    )

    return
  }

  if (executable.action) {
    const result = await runAction(
      executable.action,
      resolvedCtx
    )

    const success =
      result === true ||
      (hasStatus(result) &&
        result.status === "ok")

    const shouldReload =
      executable.reloadOnSuccess === true ||
      (
        executable.reloadOnSuccess !== false &&
        !(
          result &&
          typeof result === "object" &&
          (
            ("download" in result &&
              typeof result.download === "string") ||
            ("redirect" in result &&
              typeof result.redirect === "string")
          )
        )
      )

    if (success && shouldReload) {
      await reload?.()
    }

    return result
  }

  console.warn(
    "executeExecutable: executable must define 'to' or 'action'",
    executable
  )
}