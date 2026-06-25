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


type BulkAction = ExecutableAction & {

  key: string

  label: string

  variant?: string

  bulk?: boolean

}


function isBulkAction(
  value: unknown,
): value is BulkAction {

  if (

    !value

    ||

    typeof value !== "object"

  ) {

    return false

  }

  const action = value as {

    key?: unknown

    label?: unknown

  }

  return (

    typeof action.key ===
    "string"

    &&

    typeof action.label ===
    "string"

  )

}


function getRowId(
  row: BaseRow,
): string | number | undefined {

  if (

    typeof row.id === "string"

    ||

    typeof row.id === "number"

  ) {

    return row.id

  }

  if (

    typeof row.pk === "string"

    ||

    typeof row.pk === "number"

  ) {

    return row.pk

  }

  if (

    typeof row.uuid === "string"

    ||

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

    name:
      "bulkActions",

    phase:
      "afterList",

    apply(ctx) {

      if (

        !ctx.list

      ) {

        return ctx

      }


      /*
      🔥 старый DSL
      */

      const directActions = (

        ctx.block
          .bulkActions

        ??

        []

      ).filter(

        isBulkAction

      )


      /*
      🔥 новый DSL
      */

      const inheritedActions = (

        ctx.block
          .rowActions

        ??

        []

      ).filter(

        action =>

          isBulkAction(

            action

          )

          &&

          action.bulk === true

      )


      const actions: BulkAction[] = [

        ...directActions,

        ...inheritedActions,

      ]


      if (

        !actions.length

      ) {

        return ctx

      }


      return {

        ...ctx,


        ctrl: {


          ...ctx.ctrl,


          bulkActions:

            actions,


          onBulkAction:


            async (

              key,

              rows,

            ) => {


              const action =

                actions.find(

                  item =>

                    item.key ===

                    key

                )


              if (

                !action

              ) {

                return

              }


              const ids =

                rows

                .map(

                  getRowId

                )

                .filter(

                  (

                    value,

                  )

                  :

                  value is

                    string

                    |

                    number =>

                      value !==

                      undefined

                )


              const selection = {

                rows,

                ids,

                count:

                  rows.length,

              }


              await executeExecutable({

                entity:

                  ctx.entity,


                row: {

                  id:

                    ids[0],

                },


                executable: {

                  ...action,


                  ctx: {


                    ...(

                      action.ctx

                      ??

                      {}

                    ),


                    selection,

                  },

                },


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