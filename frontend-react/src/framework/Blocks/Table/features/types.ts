import type { ActionContext } from "@/framework/Blocks/Action/types"
import type {
  BaseRow,
  TableCapabilities,
  TableCtrlBase,
} from "../types/runtime"
import type { TableApiBlock } from "../types/api"
import type { PageApi } from "@/framework/page/context/types"
import type { ToolbarAction } from "@/framework/components/ToolBars/toolbar"

/* ========================================
   FEATURE PHASE
======================================== */

export type FeaturePhase =
  | "beforeList"
  | "afterList"

/* ========================================
   DSL (вход)
======================================== */

export type TableToolbarAction =
  | string
  | {
      label?: string

      to?: string
      action?: string
      ctx?: Record<string, unknown>

      order?: number
      disabled?: boolean
    }

/* ========================================
   LIST RUNTIME
======================================== */

export type TableListData<T extends BaseRow> = {
  fields: TableCtrlBase<T>["fields"]
  rows: TableCtrlBase<T>["rows"]

  loading: boolean

  page: {
    page: number
    pages: number
    total: number
  } | null

  capabilities: TableCapabilities

  selection?: TableCtrlBase<T>["selection"]

  reload?: () => Promise<void>

  delete?: (
    id: string | number
  ) => Promise<boolean>
}

/* ========================================
   FEATURE CONTEXT
======================================== */

export interface TableFeatureContext<
  T extends BaseRow,
  TCtrl extends TableCtrlBase<T> = TableCtrlBase<T>
> {
  block: TableApiBlock

  entity: string
  fieldset: string

  query: {
    page: number
    search: string
    sort?: string
    setPage: (p: number) => void
    setSearch: (q: string) => void
    setSort: (s: string) => void
  }

  listParams: {
    page: number
    search?: string
    sort?: string
  }

  list?: TableListData<T>

  pageApi: PageApi

  actions: {
    runAction: (
      target: string,
      ctx?: ActionContext
    ) => Promise<unknown>

    isRunning: (id: string) => boolean
  }

  ctrl: Partial<TCtrl>

  toolbar?: {
    actions?: ToolbarAction[]
    search?: {
      value: string
      onChange: (v: string) => void
    }
  }

  modals?: {
    visibleFields?: {
      isOpen: boolean
      open: () => void
      close: () => void
    }
  }
}

/* ========================================
   FEATURE INTERFACE
======================================== */

export interface TableFeature<T extends BaseRow> {
  name: string
  phase: FeaturePhase
  apply(
    ctx: TableFeatureContext<T>
  ): TableFeatureContext<T>
}