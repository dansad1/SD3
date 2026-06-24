import { resolveProps } from "@/framework/bind/expression/resolveProps"

import type { ExecutableAction } from "./types"
import { hasStatus } from "./hasStatus"
import { confirmExecutable } from "./confirmExecutable"
import { interpolateTarget } from "./interpolateTarget"
import { buildExecutableContext } from "./buildExecutableContext"

import type { BaseRow } from "../types/runtime"


export interface ExecutableRow extends BaseRow {
  selection?: {
    rows: BaseRow[]
    ids: Array<string | number>
    count: number
  }
}


type Options = {
  entity?: string

  row: ExecutableRow

  executable: ExecutableAction

  runAction: (
    target: string,
    ctx?: Record<string, unknown>,
  ) => Promise<unknown>

  reload?: () => Promise<unknown> | unknown
}


export async function executeExecutable({
  entity,
  row,
  executable,
  runAction,
  reload,
}: Options) {

  if (!confirmExecutable(executable)) {
    return
  }

  const { finalCtx } = buildExecutableContext(
    entity,
    row,
    executable,
  )

  const resolvedPropsCtx: Record<string, unknown> =
    executable.ctx
      ? resolveProps(
          executable.ctx,
          {
            ...finalCtx,
            row,
          },
        ) as Record<string, unknown>
      : {}

  const resolvedCtx = {
    ...finalCtx,
    ...resolvedPropsCtx,

    id:
      resolvedPropsCtx.id
      ?? finalCtx.id
      ?? row.id
      ?? row.name,
  }

  console.log(
    "🧾 EXECUTABLE CTX",
    {
      rawCtx: executable.ctx,
      row,
      finalCtx,
      resolvedPropsCtx,
      resolvedCtx,
    },
  )

  if (executable.to) {

    const resolvedTo = interpolateTarget(
      executable.to,
      resolvedCtx,
    )

    if (!resolvedTo) {

      console.warn(
        "executeExecutable: resolvedTo is empty",
        {
          executable,
          resolvedCtx,
          row,
        },
      )

      return
    }

    await runAction(
      resolvedTo,
      resolvedCtx,
    )

    return
  }

  if (executable.action) {

    const result = await runAction(
      executable.action,
      resolvedCtx,
    )

    const resultObj =
      typeof result === "object"
      && result !== null
        ? result as Record<string, unknown>
        : null

    const success =
      result === true
      || (
        hasStatus(result)
        && result.status === "ok"
      )

    const shouldReload =

      executable.reloadOnSuccess === true

      ||

      (

        executable.reloadOnSuccess !== false

        &&

        !(

          resultObj

          &&

          (

            typeof resultObj.download === "string"

            ||

            typeof resultObj.redirect === "string"

          )

        )

      )

    if (
      success
      &&
      shouldReload
    ) {

      await reload?.()

    }

    return result

  }

  console.warn(

    "executeExecutable: executable must define 'to' or 'action'",

    executable,

  )

}