// rowActions.ts

import type { TableFeature } from "./types"
import type { BaseRow, RowAction } from "../types/runtime"
import { executeExecutable } from "../executable/executeExecutable"


export function rowActionsFeature<T extends BaseRow>(): TableFeature<T> {
  return {
    name: "rowActions",
    phase: "afterList",

    apply(ctx) {
      if (!ctx.block.rowActions || !ctx.list) {
        return ctx
      }

      const actions = ctx.block.rowActions.filter(
        a => ctx.list?.capabilities?.[a.key] !== false
      ) as RowAction<T>[]

      return {
        ...ctx,
        ctrl: {
          ...ctx.ctrl,

          rowActions: actions,

          onRowAction: async (key: string, row: T) => {
            const action = actions.find(
              a => a.key === key
            )

            if (!action) {
              console.warn(
                "rowActions: action not found",
                key
              )
              return
            }

            console.log("🧾 ROW ACTION CLICK", {
              key,
              row,
              action,
            })

            await executeExecutable({
              entity: ctx.entity,
              row,
              executable: action,
              runAction: ctx.actions.runAction,
              reload: ctx.list?.reload,
            })
          },
        },
      }
    },
  }
}