// framework/form/types.ts

import type { FC } from "react"

/* =========================================================
   FORM VALUE
   ========================================================= */

export type Value =
  | string
  | number
  | boolean
  | string[]
  | File
  | null
    | InsertCommand

    export type InsertCommand = {
  targetField: string
  value: string
  mode: "append" | "replace"
}
/* =========================================================
   OPTION
   ========================================================= */

export type Option = {
  value: string | number
  label: string
}

/* =========================================================
   FIELD SCHEMA
   ========================================================= */

export interface FieldSchema {

  /* identity */

  id: string
  name: string

  /* UI */

  label?: string
  help_text?: string

  /* widget */

  widget: string
  html_type?: string

  /* options */

  choices?: Option[]

  /* relation */

  entity?: string
  multiple?: boolean
  columns?: number

  /* validation */

  required?: boolean
  readonly?: boolean
}

/* =========================================================
   WIDGET PROPS
   ========================================================= */

export interface WidgetProps {

  field: FieldSchema

  value: Value

  onChange: (value: Value) => void

  loading?: boolean
}

/* =========================================================
   WIDGET RENDERER
   ========================================================= */

export type WidgetRenderer = FC<WidgetProps>

/* =========================================================
   OPTION WIDGET
   ========================================================= */

export interface OptionWidgetProps {

  field: FieldSchema

  option: Option

  checked: boolean

  toggle: () => void

  loading?: boolean
}

export type OptionWidgetRenderer = FC<OptionWidgetProps>