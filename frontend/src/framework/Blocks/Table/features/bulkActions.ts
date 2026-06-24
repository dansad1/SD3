// table/features/bulkActions.ts

import {
  executeExecutable,
} from "../executable/executeExecutable"

import type {
  ExecutableAction,
} from "../executable/types"

import type {
  BaseRow,
} from "../types/runtime"

import type {
  TableFeature,
} from "./types"


function getRowId(
  row: BaseRow,
): string | number | undefined {

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
    typeof row.uuid === "string" ||
    typeof row.uuid === "number"
  ) {
    return row.uuid
  }

  return undefined
}


export function bulkActionsFeature<
  T extends BaseRow
>(): TableFeature<T> {

  return {

    name: "bulkActions",

    phase: "afterList",

    apply(ctx) {

      if (!ctx.list) {
        return ctx
      }

      const actions = (
        ctx.block.rowActions ?? []
      ).filter(
        action =>
          (action as { bulk?: boolean }).bulk === true
      )

      if (!actions.length) {
        return ctx
      }

      return {

        ...ctx,

        ctrl: {

          ...ctx.ctrl,

          bulkActions:

            actions.map(action => ({

              key:
                action.key,

              label:
                action.label,

              variant:
                action.variant,

            })),



          onBulkAction:

            async (

              key: string,

              rows: T[],

            ) => {

              const action = actions.find(

                a =>

                  a.key === key

              )

              if (!action) {
                return
              }


              const ids = rows

                .map(getRowId)

                .filter(

                  (

                    value

                  ): value is

                    string

                    |

                    number =>

                      value !== undefined

                )


              const selection = {

                rows,

                ids,

                count:

                  rows.length,

              }


              const executable: ExecutableAction = {

                ...action,


                ctx: {

                  selection,


                  ...(action.ctx ?? {}),

                },

              }


              await executeExecutable({

                entity:

                  ctx.entity,


                row: {

                  id:

                    ids[0],

                },


                executable,


                runAction:

                  ctx.actions
                    .runAction,


                reload:

                  ctx.list
                    ?.reload,

              })

            },

        },

      }

    },

  }

}