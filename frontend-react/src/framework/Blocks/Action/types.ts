import type { PageApi } from "@/framework/page/context/types"
import type { BaseBlock } from "../BlockType"


export type ActionBlock = BaseBlock & {
  type: "action"
  label: string

  to?: string
  action?: string

  ctx?: ActionContext

  variant?: "primary" | "secondary" | "ghost" | "danger"
}

export type ActionDescriptor = {
  id: string
  label: string
  variant?: "primary" | "secondary" | "ghost" | "danger"
  icon?: string

  placement?: "footer" | "header" | "form"
}
/* ========================================
   RUNTIME DATA
======================================== */

export type RuntimeRow = {
  id?: string | number
  [key: string]: unknown
}

/* ========================================
   CONTEXT (🔥 НОРМАЛИЗОВАННЫЙ)
======================================== */

export type ActionContext = {
  page?: {
    params?: Record<string, string>
    query?: Record<string, string>
        api?: PageApi // 🔥 ДОБАВИТЬ
  }

  entity?: string
  id?: string | number
  row?: RuntimeRow
  selection?: RuntimeRow[]

  data?: unknown
  form?: Record<string, unknown>

  list?: {
    reload?: () => Promise<void>
    delete?: (id: string | number) => Promise<void | boolean> // 🔥 фикс
  }

  modals?: {
    visibleFields?: {
      open: () => void
      close: () => void
    }
  }

  payload?: unknown
  extra?: Record<string, unknown>
}

/* ========================================
   HANDLERS
======================================== */

export type ActionHandler = (
  ctx: ActionContext
) => Promise<boolean> | boolean

export type ActionMap = Record<string, ActionHandler>

/* ========================================
   UPLOAD
======================================== */

