// src/framework/api/form/types.ts

import type { Json } from "@/framework/types/json"

/* =========================================================
   HTML TYPES
========================================================= */

export type ApiHtmlType =
  | "text"
  | "password"
  | "email"
  | "number"
  | "date"
  | "datetime-local"
  | "time"

/* =========================================================
   PRESENTATION
========================================================= */

export type ApiTone =
  | "neutral"
  | "success"
  | "warning"
  | "danger"
  | "info"
  | "accent"

export type ApiEmphasis =
  | "soft"
  | "normal"
  | "strong"

export type ApiMarker =
  | "active"
  | "muted"
  | "disabled"
  | "selected"

export type ApiPresentationNode = {
  tone?: ApiTone

  emphasis?: ApiEmphasis

  marker?: ApiMarker

  badge?: {
    text: string
    tone?: ApiTone
  }

  icon?: string
}

/* =========================================================
   SEMANTIC
========================================================= */

export type ApiSemanticField = {

  /**
   * semantic meaning
   *
   * examples:
   * - attendance_status
   * - person
   * - money
   * - grade
   */

  type: string

  /**
   * optional semantic role
   */

  role?: string
}

/* =========================================================
   VIEW
========================================================= */

export type ApiViewVariant =
  | "default"
  | "compact"
  | "inline"
  | "editor"
  | "readonly"
  | "analytics"
  | "card"

export type ApiViewDensity =
  | "compact"
  | "normal"
  | "comfortable"

export type ApiRenderView = {

  /**
   * visual representation intent
   */

  variant?: ApiViewVariant

  /**
   * density/layout hint
   */

  density?: ApiViewDensity
}

/* =========================================================
   option
========================================================= */

export type ApiChoice = {
  value: string | number
  label: string
}

/* =========================================================
   FORM FIELD
========================================================= */

export type ApiFormField = {

  /* identity */

  id?: string
  name: string

  /* data type */

  type?: FieldType

  /* ui */

  label?: string
  help_text?: string

  widget?: string

  semantic?: ApiSemanticField

  view?: ApiRenderView

  presentation?: ApiPresentationNode

  html_type?: ApiHtmlType

  options?: ApiChoice[]

  entity?: string
  multiple?: boolean
  columns?: number

  required?: boolean
  readonly?: boolean
}

/* =========================================================
   CAPABILITIES
========================================================= */

export type ApiFormCapabilities = {
  list?: boolean
  view?: boolean
  create?: boolean
  edit?: boolean
  delete?: boolean
}

/* =========================================================
   FORM SCHEMA
========================================================= */

export type ApiFormSchema = {

  /**
   * optional form layout
   */

  layout?:
    | "simple"
    | "tabs"
    | "split"

  fields: ApiFormField[]

  initial?: Record<string, Json>

  capabilities?: ApiFormCapabilities
}
export type FieldType =
  | "string"
  | "text"
  | "number"
  | "boolean"
  | "date"
  | "datetime"
  | "time"
  | "choice"
  | "multichoice"
  | "relation"
  | "file"
  | "json"