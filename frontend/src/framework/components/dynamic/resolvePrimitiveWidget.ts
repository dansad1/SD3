import { resolveWidgetAlias, type WidgetKey } from "./registry"
import type { FieldSchema } from "./types"

export function resolvePrimitiveWidget(
  field: FieldSchema
): WidgetKey {

  console.log(
    "🔧 RESOLVE PRIMITIVE",
    {
      name: field.name,
      type: field.type,
      widget: field.widget,
      html_type: field.html_type,
      entity: field.entity,
      multiple: field.multiple,
    }
  )

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

  console.log(
    "🔧 EXPLICIT",
    field.name,
    field.widget,
    explicit
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