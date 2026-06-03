import type {
  ApiFormSchema,
} from "@/framework/api/form/types"

import type {
  FormSchema,
} from "../types/types"

import {
  adaptField,
} from "./adaptField"

export function adaptFormSchema(
  api: ApiFormSchema
): FormSchema {

  const blocks =
    api.fields.map(
      adaptField
    )

  return {

    fields:
      blocks.map(
        block => block.field
      ),

    blocks,

    initial:
      api.initial ?? {},

    capabilities:
      api.capabilities ?? {},
  }
}