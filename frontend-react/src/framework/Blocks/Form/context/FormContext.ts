// src/Blocks/Form/FormContext.ts

import { createContext, useContext } from "react"
import type { Json } from "@/framework/types/json"
import type { FormSchema } from "../types/ui"

/* =========================
   TYPES
   ========================= */

export type FormValues = Record<string, Json>

export type FormContextValue = {
  schema: FormSchema | null
  values: FormValues

  loading: boolean
  saving: boolean
  readonly: boolean
  dirty: boolean

  setValue: (name: string, value: Json) => void

  // 🔥 ИЗМЕНЕНО
  submit: () => Promise<boolean>
}

/* =========================
   CONTEXT
   ========================= */

export const FormContext =
  createContext<FormContextValue | null>(null)

export function useFormContext(): FormContextValue {
  const ctx = useContext(FormContext)

  if (!ctx) {
    throw new Error(
      "useFormContext must be used inside <FormProvider>"
    )
  }

  return ctx
}