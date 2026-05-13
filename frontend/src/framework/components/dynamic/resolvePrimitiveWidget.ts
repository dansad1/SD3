// resolvePrimitiveWidget.ts

import type {
  FieldSchema,
} from "@/framework/components/dynamic/types"

import {
  widgetRegistry,
} from "@/framework/components/dynamic/registry"

export type WidgetKey =
  keyof typeof widgetRegistry

export function resolvePrimitiveWidget(
  field: FieldSchema
): WidgetKey {

  console.log(
    "🧠 resolvePrimitiveWidget",
    {
      name: field.name,
      widget: field.widget,
      html_type: field.html_type,
      field,
    }
  )

  /* ========================================
     html_type priority
  ======================================== */

  if (field.html_type === "password") {
    console.log("🔐 PASSWORD DETECTED")
    return "PasswordInput"
  }

  if (field.html_type === "number") {
    return "NumberInput"
  }

  if (field.html_type === "date") {
    return "DateInput"
  }

  if (field.html_type === "datetime-local") {
    return "DateTimeInput"
  }

  if (field.html_type === "time") {
    return "TimeInput"
  }

  /* ========================================
     explicit widget
  ======================================== */

  switch (field.widget) {

    case "TextInput":
    case "Textarea":
    case "NumberInput":
    case "Checkbox":
    case "Select":
    case "MultiSelect":
    case "DateInput":
    case "DateTimeInput":
    case "TimeInput":
    case "FileInput":
    case "PasswordInput":
    case "RichText":
    case "InsertVariables":
      return field.widget
  }

  /* ========================================
     entity fallback
  ======================================== */

  if (field.entity) {

    if (
      field.multiple
      && field.columns
    ) {
      return "Checkbox"
    }

    if (field.multiple) {
      return "MultiSelect"
    }

    return "Select"
  }

  /* ========================================
     default
  ======================================== */

  return "TextInput"
}