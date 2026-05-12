import type {
  ApiFormSchema,
} from "@/framework/api/form/types"

import type {
  FormSchema,
} from "../types/types"
import { adaptField } from "./adaptField"



export function adaptFormSchema(
  api: ApiFormSchema
): FormSchema {

  return {

    blocks:
      api.fields.map(
        adaptField
      ),

    initial:
      api.initial ?? {},
  }
}