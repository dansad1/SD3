import type {
  ApiFormField,
} from "@/framework/api/form/types"

import type {
  FieldSchema,
} from "@/framework/components/dynamic/types"

import type {
  FormFieldBlock,
} from "../types/types"

import {
  resolveWidget,
} from "@/framework/components/dynamic/widgets/resolveWidget"

export function adaptField(
  field: ApiFormField
): FormFieldBlock {

  const id =
    field.id ??
    field.name

  const widget =
    resolveWidget({
      ...field,
      id,
    } as FieldSchema)

  return {

    id,

    type: "field",

    field: {

      ...field,

      id,

      widget,

    } as FieldSchema,

  }
}
export function adaptFieldSchema(
  field: ApiFormField
): FieldSchema {

  const id =
    field.id ??
    field.name

  const schema: FieldSchema = {
    ...field,
    id,
    widget: "",
  } as FieldSchema

  schema.widget =
    resolveWidget(schema)

  return schema
}