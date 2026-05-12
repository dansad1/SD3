import type { FC, CSSProperties } from "react"

/* =========================================================
   FORM VALUE
========================================================= */

export type InsertCommand = {
  targetField: string
  value: string
  mode: "append" | "replace"
}

export type Value =
  | string
  | number
  | boolean
  | string[]
  | File
  | null
  | InsertCommand

/* =========================================================
   OPTION
========================================================= */

export type Option = {
  value: string | number
  label: string
}

/* =========================================================
   PRESENTATION
========================================================= */

export type Tone =
  | "neutral"
  | "success"
  | "warning"
  | "danger"
  | "info"
  | "accent"

export type Emphasis =
  | "soft"
  | "normal"
  | "strong"

export type Marker =
  | "active"
  | "muted"
  | "disabled"
  | "selected"

export type PresentationNode = {
  tone?: Tone
  emphasis?: Emphasis
  marker?: Marker

  badge?: {
    text: string
    tone?: Tone
  }

  icon?: string
}

/* =========================================================
   SEMANTIC
========================================================= */

export type SemanticField = {
  type: string
  role?: string
}

/* =========================================================
   VIEW INTENT
========================================================= */

export type ViewVariant =
  | "default"
  | "compact"
  | "inline"
  | "editor"
  | "readonly"
  | "analytics"
  | "card"

export type ViewDensity =
  | "compact"
  | "normal"
  | "comfortable"

export type RenderView = {
  variant?: ViewVariant
  density?: ViewDensity
}

/* =========================================================
   RUNTIME CONTEXT
========================================================= */

export type RenderContext =
  | "form"
  | "table"
  | "details"
  | "matrix"
  | "analytics"
  | "card"

export type Platform =
  | "desktop"
  | "mobile"
  | "tablet"

export type InteractionMode =
  | "readonly"
  | "editable"
  | "quick-edit"
  | "inline-edit"

/* =========================================================
   FIELD SCHEMA
========================================================= */

export interface FieldSchema {
  id: string
  name: string

  label?: string
  help_text?: string

  /**
   * primitive fallback
   */
  widget?: string

  /**
   * what it is
   */
  semantic?: SemanticField

  /**
   * how it should be represented
   */
  view?: RenderView

  /**
   * visual appearance only
   */
  presentation?: PresentationNode

  html_type?: string

  choices?: Option[]

  entity?: string
  multiple?: boolean
  columns?: number

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

  context?: RenderContext
  platform?: Platform
  interaction?: InteractionMode

  view?: RenderView
  presentation?: PresentationNode

  readonly?: boolean

  errors?: string[]
}

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

  presentation?: PresentationNode
}

export type OptionWidgetRenderer =
  FC<OptionWidgetProps>

/* =========================================================
   FIELD APPEARANCE
========================================================= */

export type ResolvedFieldAppearance = {
  className?: string
  style?: CSSProperties
  hidden?: boolean
}