import type { Json } from "@/framework/types/json"
import type { FieldSchema } from "@/framework/components/dynamic/types"

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

export type FormGroupMode =
  | "sections"
  | "tabs"

export type FormLayout = {
  preset?: FormLayoutPreset

  density?: FormDensity

  groups?: FormGroupMode
}

export type FormBlockLayout = {
  span?: 1 | 2 | 3 | 4 | 6 | 12
  order?: number
  hidden?: boolean
}

export type FormFieldBlock = {
  id: string
  type: "field"
  field: FieldSchema
  layout?: FormBlockLayout
}

export type FormSectionBlock = {
  id: string
  type: "section"
  title?: string
  description?: string
  layout?: FormBlockLayout
  children: FormBlock[]
}

export type FormStackBlock = {
  id: string
  type: "stack"
  gap?: "none" | "sm" | "md" | "lg"
  layout?: FormBlockLayout
  children: FormBlock[]
}

export type FormTabsBlock = {
  id: string
  type: "tabs"
  variant?: "line" | "pills" | "segmented"
  layout?: FormBlockLayout
  children: FormBlock[]
}

export type FormBlock =
  | FormFieldBlock
  | FormSectionBlock
  | FormStackBlock
  | FormTabsBlock

export type ApiFormFieldBlock = {
  id?: string
  type: "field"
  field: string
  layout?: FormBlockLayout
}

export type ApiFormSectionBlock = {
  id?: string
  type: "section"
  key?: string
  title?: string
  description?: string
  layout?: FormBlockLayout
  children?: ApiFormBlock[]
}

export type ApiFormStackBlock = {
  id?: string
  type: "stack"
  gap?: "none" | "sm" | "md" | "lg"
  layout?: FormBlockLayout
  children?: ApiFormBlock[]
}

export type ApiFormTabsBlock = {
  id?: string
  type: "tabs"
  variant?: "line" | "pills" | "segmented"
  layout?: FormBlockLayout
  children?: ApiFormBlock[]
}

export type ApiFormBlock =
  | ApiFormFieldBlock
  | ApiFormSectionBlock
  | ApiFormStackBlock
  | ApiFormTabsBlock

export type FormSchema = {
  entity?: string
  model?: string
  fields: FieldSchema[]
  blocks?: ApiFormBlock[] | FormBlock[]
  initial?: Record<string, Json>
  layout?: FormLayout
  capabilities?: Record<string, boolean>
}

export function isFieldBlock(
  block: FormBlock
): block is FormFieldBlock {
  return block.type === "field"
}

export function isSectionBlock(
  block: FormBlock
): block is FormSectionBlock {
  return block.type === "section"
}

export function isStackBlock(
  block: FormBlock
): block is FormStackBlock {
  return block.type === "stack"
}

export function isTabsBlock(
  block: FormBlock
): block is FormTabsBlock {
  return block.type === "tabs"
}