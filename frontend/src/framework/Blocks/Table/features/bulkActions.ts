// table/features/bulkActions.ts

import { executeExecutable } from "../executable/executeExecutable"
import type { ExecutableAction } from "../executable/types"
import type { BaseRow } from "../types/runtime"
import type { TableFeature } from "./types"


export function bulkActionsFeature<
  T extends BaseRow
>(): TableFeature<T> {
  return {
    name: "bulkActions",
    phase: "afterList",

    apply(ctx) {
      if (
        !Array.isArray(
          ctx.block.bulkActions
        ) ||
        !ctx.list
      ) {
        return ctx
      }

      const actions =
        ctx.block.bulkActions.filter(
          (
            action
          ): action is ExecutableAction & {
            key: string
          } => {
            if (
              !action ||
              typeof action !== "object"
            ) {
              return false
            }

            const typedAction =
              action as ExecutableAction & {
                key?: string
              }

            if (!typedAction.key) {
              return false
            }

            return (
              ctx.list?.capabilities?.[
                typedAction.key
              ] !== false
            )
          }
        )

      return {
        ...ctx,
        ctrl: {
          ...ctx.ctrl,

          bulkActions: actions,

          onBulkAction: async (
            key: string,
            rows: T[]
          ) => {
            const action = actions.find(
              a => a.key === key
            )

            if (!action) {
              console.warn(
                "bulkActions: action not found",
                key
              )
              return
            }

            const ids = rows
              .map(row => {
                if (
                  typeof row.id === "string" ||
                  typeof row.id === "number"
                ) {
                  return row.id
                }

                if (
                  typeof row.pk === "string" ||
                  typeof row.pk === "number"
                ) {
                  return row.pk
                }

                if (
                  typeof row.uuid ===
                    "string" ||
                  typeof row.uuid ===
                    "number"
                ) {
                  return row.uuid
                }

                return undefined
              })
              .filter(
                (
                  value
                ): value is string | number =>
                  value !== undefined
              )

            const selection = {
              rows,
              ids,
              count: rows.length,
            }

            await executeExecutable({
              entity: ctx.entity,

              row: {
                id: ids[0],
                selection,
              } as unknown as T,

              executable: {
                ...action,

                ctx: {
                  selection,
                  ...(action.ctx || {}),
                },
              },

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