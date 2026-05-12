// src/framework/blocks/form/runtime.ts

import type { Json } from "@/framework/types/json"
import type { FormSchema as UiFormSchema } from "./ui"

export type EntityFormMode = "create" | "edit" | "view"

/* ================= COMPILED CONFIG ================= */


/* ================= RUNTIME VIEW ================= */

export type FormRuntimeView = {
  loading: boolean
  dirty: boolean
  readonly: boolean

  values: Record<string, Json>
  setValue: (id: string, v: Json) => void

  schema: UiFormSchema | null

  validate?: () => boolean
  submit: () => Promise<boolean>
}