import type { Json } from "@/framework/types/json"
import type { EntityFormMode } from "./runtime"

/* ================= SUBMIT ================= */

export type FormSubmitConfig = {
  label?: string
  redirect?: string
}

/* ================= LAYOUT ================= */

export type FormLayoutPreset =
  | "default"
  | "two-columns"
  | "single-column"
  | "wide"

export type FormDensity =
  | "comfortable"
  | "default"
  | "compact"
  | "dense"

export type FormLayoutConfig = {
  preset?: FormLayoutPreset
  density?: FormDensity
}

/* ================= CONFIG ================= */

export type FormEntityConfig = {
  formType: "entity"
  entity: string

  mode?: EntityFormMode
  objectId?: string | number

  initial?: Record<string, Json>

  // ✅ ЕДИНСТВЕННОЕ ПОЛЕ
  formLayout?: FormLayoutConfig

  submit?: FormSubmitConfig
  bind?: Record<string, Json>
}

export type FormActionConfig = {
  formType: "action"
  schema: string

  submit?:
    | string
    | {
        action: string
        label?: string
        redirect?: unknown
      }

  formLayout?: FormLayoutConfig

  bind?: Record<string, Json>
}

export type FormConfig =
  | FormEntityConfig
  | FormActionConfig