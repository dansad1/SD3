import { resolveFieldWidget } from "../components/dynamic/resolveFieldWidget"
import type { FieldSchema, RenderView } from "../components/dynamic/types"


export function resolveFieldView(
  field: FieldSchema
): RenderView {

  if (field.view) {
    return field.view
  }

  const widget =
    resolveFieldWidget(
      field,
      "form",
      "desktop",
    )

  switch (widget) {

    case "Checkbox":

      return {
        variant: "inline",
      }

    default:

      return {
        variant: "default",
      }
  }
}