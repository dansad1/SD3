import type {
  ApiFormField,
} from "@/framework/api/form/types"

import type {
  FieldBlock,
} from "../types/types"
import { resolveWidget } from "@/framework/components/dynamic/widgets/resolveWidget"


export function adaptField(
  field: ApiFormField
): FieldBlock {

  const id =
    field.id ||
    field.name

  const widget =
    resolveWidget(field)

  return {

    id,

    type: "field",

    field: {

      id,

      name:
        field.name,

      label:
        field.label,

      help_text:
        field.help_text,

      widget,

      semantic:
        field.semantic,

      view:
        field.view,

      presentation:
        field.presentation,

      html_type:
        field.html_type,

      choices:
        field.choices,

      entity:
        field.entity,

      multiple:
        field.multiple,

      columns:
        field.columns,

      required:
        field.required,

      readonly:
        field.readonly,
    },
  }
}