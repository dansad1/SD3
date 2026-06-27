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
export type PickerConfig = {
    entity: string

    title?: string

    multiple?: boolean

    filter?: Record<
        string,
        unknown
    >
}
/* =========================================================
   ACTION BLOCK
========================================================= */

export type ActionBlock = BaseBlock & {
  type: "action"
  label: string
  icon?: string
  to?: string
    picker?: PickerConfig   // <-- ЭТОГО сейчас нет

  /**
   * Backend action code
   */
  action?: string
  ctx?: ActionContext

  
  variant?: ActionVariant

  
  capabilities?: BlockCapabilities
  confirm?:
    | boolean
    | {
        message?: string
      }

  refresh?: string[]
  closeModal?: boolean
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
picker?: PickerConfig
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

export type ModalController = {

    isOpen: boolean

    open: () => void

    close: () => void

}

export type ModalsContext = {

    visibleFields?: ModalController

    filters?: ModalController

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