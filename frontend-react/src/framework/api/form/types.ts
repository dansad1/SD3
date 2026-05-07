// src/framework/api/form/types.ts
import type { Json } from "@/framework/types/json"

export type ApiHtmlType =
  | "text"
  | "password"
  | "email"
  | "number"
  | "date"
  | "datetime-local"
  | "time" // 👈 добавь

export type ApiFormField = {
  id?: string
  name: string
  label?: string
  help_text?: string
  widget: string
  html_type?: ApiHtmlType
  choices?: {
    value: string | number
    label: string
  }[]
  entity?: string
  multiple?: boolean
  columns?: number
  required?: boolean
  readonly?: boolean
}

export type ApiFormCapabilities = {
  list?: boolean
  view?: boolean
  create?: boolean
  edit?: boolean
  delete?: boolean
}

export type ApiFormSchema = {
  layout?: "simple" | "tabs" | "split"
  fields: ApiFormField[]
  initial?: Record<string, Json>
  capabilities?: ApiFormCapabilities
}