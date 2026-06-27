import { resolveWidgetAlias, type WidgetKey } from "./registry"
import type { FieldSchema } from "./types"

export function resolvePrimitiveWidget(
  field: FieldSchema
): WidgetKey {

  

  switch (field.html_type) {

    case "password":
      return "PasswordInput"

    case "number":
      return "NumberInput"

    case "date":
      return "DateInput"

    case "datetime-local":
      return "DateTimeInput"

    case "time":
      return "TimeInput"
  }

  const explicit =
    resolveWidgetAlias(
      field.widget
    )

  

  if (explicit) {
    return explicit
  }

  if (field.entity) {

    if (field.multiple) {
      return "MultiSelect"
    }

    return "Select"
  }

  return "TextInput"
}