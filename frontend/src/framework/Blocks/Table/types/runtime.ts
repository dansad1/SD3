import type { ReactNode } from "react"
import type { Json } from "@/framework/types/json"

/* ================= BASE ROW ================= */

export type BaseRow =
  { id: string | number } & Record<string, Json>

/* ================= CAPABILITIES ================= */

export type TableCapabilities = {
  search?: boolean
  selection?: boolean
  sorting?: boolean

  [actionKey: string]: boolean | undefined
}

/* ================= FIELD META ================= */

export interface ListFieldMeta {
  key: string
  label: ReactNode

  width?: number | string

  sortable?: boolean
  clickable?: boolean

  onClick?: () => void
}

/* ================= ROW ACTION ================= */

// table/types.ts

export interface RowAction<T = unknown> {
  key: string
  label: string

  variant?: "primary" | "secondary" | "ghost" | "danger"

  action?: string
  to?: string

  ctx?: Record<string, Json>
  params?: Record<string, Json>

  run?: string | ((row: T) => string)

  confirm?: boolean | { message: string }
}
/* ================= TABLE CTRL ================= */

export interface TableCtrlBase<T extends BaseRow> {
  fields: ListFieldMeta[]
  rows: T[]

  isLoading?: boolean
  error?: string | null

  capabilities?: TableCapabilities

  sort?: {
    key: string
    direction: "asc" | "desc"
    set: (key: string) => void
  }

  selection?: {
    selected: Set<string | number>
    toggle: (id: string | number) => void
    toggleAll: () => void
    clear: () => void
    isAllSelected: boolean
  }

  rowActions?: RowAction<T>[]

  onRowAction?: (key: string, row: T) => void
  onRowClick?: (row: T) => void
  onToolbarAction?: (key: string) => void
}