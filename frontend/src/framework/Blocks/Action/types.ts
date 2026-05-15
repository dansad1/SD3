import type { PageApi } from "@/framework/page/context/types"
import type { BaseBlock, BlockCapabilities } from "../BlockType"

/* =========================================================
   COMMON
========================================================= */

export type ActionVariant =
  | "primary"
  | "secondary"
  | "ghost"
  | "danger"

/* =========================================================
   ACTION BLOCK
========================================================= */

export type ActionBlock = BaseBlock & {
  type: "action"

  /**
   * UI
   */
  label: string
  icon?: string

  /**
   * Navigation
   */
  to?: string

  /**
   * Backend action code
   */
  action?: string

  /**
   * Runtime context
   */
  ctx?: ActionContext

  /**
   * Visual style
   */
  variant?: ActionVariant

  /**
   * UI permissions
   *
   * examples:
   *
   * {
   *   run: true
   * }
   */
  capabilities?: BlockCapabilities

  /**
   * Optional confirmation
   */
  confirm?:
    | boolean
    | {
        message?: string
      }

  /**
   * Reload sources after success
   */
  refresh?: string[]

  /**
   * Close modal after success
   */
  closeModal?: boolean

  /**
   * Disable button
   *
   * IMPORTANT:
   * disabled !== permission
   */
  disabled?: boolean
}

/* =========================================================
   ACTION DESCRIPTOR
========================================================= */

export type ActionDescriptor = {
  id: string

  label: string

  icon?: string

  variant?: ActionVariant

  placement?:
    | "footer"
    | "header"
    | "form"

  /**
   * UI capabilities
   */
  capabilities?: BlockCapabilities

  /**
   * Optional visibility
   */
  hidden?: boolean

  /**
   * Optional disabled state
   */
  disabled?: boolean
}

/* =========================================================
   RUNTIME ROW
========================================================= */

export type RuntimeRow = {
  id?: string | number
  [key: string]: unknown
}

/* =========================================================
   PAGE CONTEXT
========================================================= */

export type PageContext = {
  params?: Record<string, string>
  query?: Record<string, string>

  /**
   * page runtime api
   */
  api?: PageApi
}

/* =========================================================
   LIST CONTEXT
========================================================= */

export type ListContext = {
  reload?: () => Promise<void>

  delete?: (
    id: string | number
  ) => Promise<void | boolean>

  capabilities?: BlockCapabilities
}

/* =========================================================
   MODALS CONTEXT
========================================================= */

export type ModalsContext = {
  visibleFields?: {
    open: () => void
    close: () => void
  }
}

/* =========================================================
   ACTION CONTEXT
========================================================= */

export type ActionContext = {

  /* =========================
     PAGE
  ========================= */

  page?: PageContext

  /* =========================
     ENTITY
  ========================= */

  entity?: string

  id?: string | number

  /* =========================
     TABLE
  ========================= */

  row?: RuntimeRow

  selection?: RuntimeRow[]

  /* =========================
     FORM
  ========================= */

  form?: Record<string, unknown>

  data?: unknown

  payload?: unknown

  /* =========================
     LIST
  ========================= */

  list?: ListContext

  /* =========================
     MODALS
  ========================= */

  modals?: ModalsContext

  /* =========================
     RUNTIME
  ========================= */

  capabilities?: BlockCapabilities

  /**
   * raw extra runtime data
   */
  extra?: Record<string, unknown>
}

/* =========================================================
   HANDLERS
========================================================= */

export type ActionHandler = (
  ctx: ActionContext
) => Promise<boolean> | boolean

export type ActionMap =
  Record<string, ActionHandler>