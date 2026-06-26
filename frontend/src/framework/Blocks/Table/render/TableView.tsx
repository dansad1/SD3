// src/framework/Blocks/Table/render/TableView.tsx

import Table from "@/framework/Blocks/Table/render/Table"

import VisibleFieldsModal
  from "@/framework/components/modals/VisibleFieldsModal/VisibleFieldsModal"



import { BlockToolbar }
  from "@/framework/components/ToolBars/ListToolbar"

import type {
  TableFeatureContext,
} from "../features/types"

import type {
  BaseRow,
} from "../types/runtime"

import { useActionExecutor }
  from "../../Action/executor/useActionExecutor"

import { Pagination }
  from "@/framework/components/ui/pagination"
import FilterModal from "@/framework/components/modals/FilterModal/FilterModal"


type Props<T extends BaseRow> = {
  ctx: TableFeatureContext<T>
}


export function TableView<
  T extends BaseRow
>({
  ctx,
}: Props<T>) {

  const {
    runAction,
  } = useActionExecutor()

  const toolbar =
    ctx.toolbar ?? {}

  const ctrl =
    ctx.ctrl ?? {}

  const list =
    ctx.list

  const fields =
    list?.fields ?? []

  const rows =
    list?.rows ?? []

  const isLoading =
    list?.loading ?? false

  const error =
    list?.error ?? null

  const pagination =
    ctrl.pagination

  const selected =
    ctrl.selection?.selected
    ?? new Set()

  const selectedRows =
    rows.filter(
      row => selected.has(
        row.id
      )
    )

  const selectedCount =
    selectedRows.length


  const handleSaved = () => {

    void list?.reload?.()

  }


  async function handleBulkAction(
    key: string,
  ) {

    await ctrl
      .onBulkAction?.(

        key,

        selectedRows as T[],

      )

    ctrl
      .selection
      ?.clear()

  }


  return (

    <>

      <BlockToolbar

        actions={
          toolbar.actions ?? []
        }

        search={
          toolbar.search
        }

        onAction={(a) => {

          const target =
            a.action ?? a.to

          if (!target) {
            return
          }

          void runAction(

            target,

            a.ctx,

          )

        }}

      />


      {

        selectedCount > 0

        &&

        (ctrl.bulkActions?.length ?? 0) > 0

        && (

          <div

            className="table-selection-panel"

          >

            <div>

              Выбрано{" "}

              <b>

                {

                  selectedCount

                }

              </b>

            </div>


            <div

              style={{

                display:
                  "flex",

                gap:
                  8,

              }}

            >

              {

                ctrl.bulkActions!.map(

                  action => (

                    <button

                      key={

                        action.key

                      }

                      type="button"

                      className={

                        `ui-btn ui-btn-${

                          action.variant

                          ??

                          "secondary"

                        }`

                      }

                      onClick={() => {

                        void handleBulkAction(

                          action.key,

                        )

                      }}

                    >

                      {

                        action.label

                      }

                    </button>

                  )

                )

              }

            </div>

          </div>

        )

      }


      <Table

        ctrl={{
          ...ctrl,
          fields,
          rows,
          isLoading,
          error,
        }}
      />

      {
        pagination &&
        <Pagination
          page={
            pagination.page
          }

          pages={
            pagination.pages
          }

          total={
            pagination.total
          }

          pageSize={
            pagination.pageSize
          }
          onChange={
            pagination.setPage
          }

        />

      }

      {

        ctx.modals
          ?.visibleFields

        && (

          <VisibleFieldsModal

            isOpen={

              ctx.modals
                .visibleFields
                .isOpen

            }

            onClose={

              ctx.modals
                .visibleFields
                .close

            }

            entity={
              ctx.entity
            }

            fieldset={
              ctx.fieldset
            }

            onSaved={
              handleSaved
            }

          />

        )

      }


      {

        ctx.modals
          ?.filters

        && (

          <FilterModal

isOpen={

ctx.modals

?.filters

?.isOpen

?? false

}


onClose={

ctx.modals

?.filters

?.close

?? (()=>{})

}


entity={

ctx.entity

}


fieldset={

ctx.fieldset

}


initialQuery={

ctx.query.filters

}


onApply={

query=>{

ctx.query

.setFilters(

query

)

}

}

/>
        )
      }
    </>
  )
}