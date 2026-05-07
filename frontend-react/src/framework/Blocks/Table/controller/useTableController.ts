// useTableController.ts

import { useState } from "react"

import { usePageApi } from "@/framework/page/context/usePageApi"
import { useResolvedRuntimeProps } from "@/framework/bind/runtime/useResolvedRuntimeProps"

import { useTableQueryRuntime } from "./useTableQueryRuntime"
import { useTableDataRuntime } from "./useTableDataRuntime"

import { applyTableFeatures } from "../features/apply"
import { collectTableFeatures } from "../features/collectFeatures"

import type { TableApiBlock } from "../types/api"
import type { BaseRow } from "../types/runtime"
import type { TableFeatureContext } from "../features/types"

import { useActionExecutor } from "../../Action/executor/useActionExecutor"
import { useTableData } from "../../Data/TableAdapter"

export function useTableController<T extends BaseRow>(
  block: TableApiBlock
) {
  const pageApi = usePageApi()

  const query = useTableQueryRuntime()
  const { runAction, isRunning } = useActionExecutor()

  const [visibleFieldsOpen, setVisibleFieldsOpen] =
    useState(false)

  // IMPORTANT:
  // row-level expressions must stay unresolved here
  // because $row.* is unavailable on page runtime level
  const resolvedBlock = useResolvedRuntimeProps({
    ...block,

    rowClick: block.rowClick,
    rowActions: block.rowActions,
    bulkActions: block.bulkActions,
  }) as TableApiBlock

  const isInlineMode =
    resolvedBlock.data !== undefined

  const baseCtx: TableFeatureContext<T> = {
    block: resolvedBlock,
    entity: resolvedBlock.entity ?? "",
    fieldset: resolvedBlock.fieldset ?? "default",

    query,

    listParams: {
      page: query.page,
      ...(resolvedBlock.filter ?? {}),
    },

    pageApi,

    ctrl: {},
    toolbar: {},

    actions: {
      runAction,
      isRunning,
    },

    modals: {
      visibleFields: {
        isOpen: visibleFieldsOpen,
        open: () => setVisibleFieldsOpen(true),
        close: () => setVisibleFieldsOpen(false),
      },
    },
  }

  const features = collectTableFeatures<T>(
    resolvedBlock
  )

  const ctxBefore = applyTableFeatures(
    baseCtx,
    features,
    "beforeList"
  )

  const resolvedParams = useResolvedRuntimeProps(
    ctxBefore.listParams
  )

  const entityList = useTableDataRuntime<T>(
    resolvedBlock.entity ?? "__disabled__",
    resolvedParams,
    {
      enabled:
        !isInlineMode &&
        !!resolvedBlock.entity,
    }
  )

  const inlineList = useTableData<T>(
    {
      entity: resolvedBlock.entity,
      data: resolvedBlock.data,
    },
    resolvedParams
  )

  const list = isInlineMode
    ? inlineList
    : entityList

  const ctxAfter = applyTableFeatures(
    {
      ...ctxBefore,
      list,
    },
    features,
    "afterList"
  )

  return ctxAfter
}