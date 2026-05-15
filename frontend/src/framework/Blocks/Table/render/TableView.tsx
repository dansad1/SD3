// src/framework/Blocks/Table/render/TableView.tsx

import Table from "@/framework/components/ui/Table"
import VisibleFieldsModal from "@/framework/components/modals/VisibleFieldsModal/VisibleFieldsModal"
import { BlockToolbar } from "@/framework/components/ToolBars/ListToolbar"

import type { TableFeatureContext } from "../features/types"
import type { BaseRow } from "../types/runtime"

import { useActionExecutor }
  from "../../Action/executor/useActionExecutor"

type Props<T extends BaseRow> = {
  ctx: TableFeatureContext<T>
}

export function TableView<
  T extends BaseRow
>({
  ctx,
}: Props<T>) {

  const { runAction } =
    useActionExecutor()

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

  const handleSaved = () => {

    void list?.reload?.()

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
            a.ctx
          )
        }}
      />

      <Table
        ctrl={{

          ...ctrl,

          fields,

          rows,

          isLoading,

          error,

        }}
      />

      {ctx.modals?.visibleFields && (

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

      )}

    </>
  )
}