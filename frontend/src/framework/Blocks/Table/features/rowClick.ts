// table/features/rowClick.ts

import { executeExecutable } from "../executable/executeExecutable"
import type { ExecutableAction } from "../executable/types"
import type { BaseRow } from "../types/runtime"
import type { TableFeature } from "./types"


export function rowClickFeature<
  T extends BaseRow
>(): TableFeature<T> {
  return {
    name: "rowClick",
    phase: "afterList",

    apply(ctx) {
      if (!ctx.block.features?.rowClick) {
        return ctx
      }

      return {
        ...ctx,
        ctrl: {
          ...ctx.ctrl,

          onRowClick: async (row: T) => {
            console.log("ROW", row)

            let executable:
              | ExecutableAction
              | null = null

            if (
              ctx.block.rowClick &&
              typeof ctx.block.rowClick ===
                "object"
            ) {
              const rowClick =
                ctx.block.rowClick as ExecutableAction

              executable = {
                ...rowClick,

                to:
                  rowClick.to ??
                  ctx.block.to ??
                  (typeof row.to === "string"
                    ? row.to
                    : undefined),
              }
            } else if (ctx.block.to) {
              executable = {
                to: ctx.block.to,
              }
            } else if (
              typeof row.to === "string"
            ) {
              executable = {
                to: row.to,
              }
            } else if (ctx.entity) {
              executable = {
                to: `${ctx.entity}:form`,
              }
            }

            console.log(
              "ROW_CLICK_EXECUTABLE",
              executable
            )

            if (!executable) {
              console.warn(
                "rowClickFeature: no executable",
                {
                  row,
                  block: ctx.block,
                }
              )
              return
            }

            await executeExecutable({
              entity: ctx.entity,
              row,
              executable,
              runAction:
                ctx.actions.runAction,
              reload:
                ctx.list?.reload,
            })
          },
        },
      }
    },
  }
}