import type { ActionContext } from "../../Action/types"
import type { BaseBlock } from "../../BlockType"
import type { TableToolbarAction } from "../features/types"
import type {
  BaseRow,
  ListFieldMeta,
  TableCapabilities,
} from "./runtime"

/* ================= PAGE INFO ================= */

export type PageInfo = {
  page: number
  pages: number
  total: number
}

/* ================= API RESPONSE ================= */

export type ApiListResponse<TRow extends BaseRow> = {
  /** 🔥 нормализованный ответ (рекомендуется на бэке) */
  items: TRow[]

  /** ⚠️ временная совместимость (можно удалить позже) */
  rows?: TRow[]

  fields: ListFieldMeta[]
  page: PageInfo

  capabilities?: TableCapabilities
}

/* ================= TOOLBAR ================= */



/* ================= ROW ACTION ================= */

export type TableApiRowAction = {
  key: string
  label: string

  variant?: "primary" | "secondary" | "ghost" | "danger"

  confirm?: boolean | { message: string }

  /** навигация */
  to?: string

  /** backend / UI action */
  action?: string

  /** 🔥 ВОТ ЭТО ДОБАВИТЬ */
  params?: Record<string, string | number | boolean>

  ctx?: ActionContext
}

/* ================= TABLE BLOCK ================= */

export type TableApiBlock = BaseBlock & {
  type: "table"

  /** CRUD режим */
  entity?: string

  fieldset?: string

  /** 🔥 кастомный источник данных */
  data?: unknown

  /** фильтры */
  filter?: Record<string, unknown>

  features?: {
    toolbar?: boolean
    search?: boolean
    selection?: boolean
    rowClick?: boolean
    rowActions?: boolean
    visibleFields?: boolean
  }

  toolbar?: {
    actions?: TableToolbarAction[]
  }

  rowActions?: TableApiRowAction[]

  bulkActions?: unknown[]

  searchableFields?: string[]

  selectionActions?: unknown[]

  rowClick?: boolean

  to?: string
}