import type { ApiFormField, ApiFormSchema } from "@/framework/api/form/types"
import { widgetRegistry } from "@/framework/components/dynamic/registry"
import type { FieldBlock, FormSchema } from "../types/types"

type WidgetKey = keyof typeof widgetRegistry

function resolveWidget(field: ApiFormField): WidgetKey {
  switch (field.widget) {
    case "TextInput":
    case "Textarea":
    case "NumberInput":
    case "Checkbox":
    case "Select":
    case "MultiSelect":
    case "DateInput":
    case "DateTimeInput":
    case "TimeInput": // 👈 добавили
    case "FileInput":
    case "PasswordInput":
    case "RichText":
      return field.widget
  }

  if (field.entity) {
    if (field.multiple && field.columns) return "Checkbox"
    if (field.multiple) return "MultiSelect"
    return "Select"
  }

  if (field.html_type === "password") return "PasswordInput"
  if (field.html_type === "number") return "NumberInput"
  if (field.html_type === "date") return "DateInput"
  if (field.html_type === "datetime-local") return "DateTimeInput"
  if (field.html_type === "time") return "TimeInput" // 👈 добавили

  return "TextInput"
}
function adaptField(field: ApiFormField): FieldBlock {
  const id = field.id || field.name
  const widget = resolveWidget(field)

  return {
    id,
    type: "field",
    field: {
      id,
      name: field.name,
      label: field.label,
      help_text: field.help_text,

      widget,

      html_type: field.html_type,
      choices: field.choices,

      entity: field.entity,
      multiple: field.multiple,
      columns: field.columns,

      required: field.required,
      readonly: field.readonly,
    },
  }
}

export function adaptFormSchema(api: ApiFormSchema): FormSchema {
  return {
    blocks: api.fields.map(adaptField),
    initial: api.initial ?? {},
  }
}