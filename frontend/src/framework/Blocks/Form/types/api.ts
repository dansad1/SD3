import type { Json } from "@/framework/types/json"
import type { BaseBlock } from "../../BlockType"
import type { FormLayoutConfig, FormSubmitConfig } from "./FormConfig"
import type { EntityFormMode } from "./runtime"

export type FormApiBlock =
  | (BaseBlock & {
      type: "form"
      entity: string
      mode?: EntityFormMode
      initial?: Record<string, Json>
      objectId?: string | number
  formLayout?: FormLayoutConfig
      submit?: FormSubmitConfig
      bind?: Record<string, Json>
    })
  | (BaseBlock & {
      type: "form"
      schema: string
      submit: string
  formLayout?: FormLayoutConfig
      bind?: Record<string, Json>
    })