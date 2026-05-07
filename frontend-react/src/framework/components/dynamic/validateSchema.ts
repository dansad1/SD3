import { widgetRegistry } from "./registry"
import type { FieldSchema } from "./types"

export function validateFieldSchema(field: FieldSchema) {
  if (!field || typeof field !== "object") {
    throw new Error(`Invalid field schema`)
  }

  if (!field.name || typeof field.name !== "string") {
    throw new Error(`Field must have a valid "name"`)
  }

  if (!field.widget || typeof field.widget !== "string") {
    throw new Error(
      `Field "${field.name}" has no valid widget`
    )
  }

  if (!widgetRegistry[field.widget]) {
    throw new Error(
      `Unknown widget "${field.widget}" in field "${field.name}"`
    )
  }

  if (field.choices && !Array.isArray(field.choices)) {
    throw new Error(
      `Invalid choices for field "${field.name}"`
    )
  }

  if (field.label && typeof field.label !== "string") {
    throw new Error(
      `Invalid label for field "${field.name}"`
    )
  }

  if (field.required && typeof field.required !== "boolean") {
    throw new Error(
      `Invalid required flag in field "${field.name}"`
    )
  }

  if (field.readonly && typeof field.readonly !== "boolean") {
    throw new Error(
      `Invalid readonly flag in field "${field.name}"`
    )
  }

  /* ===============================
     multiple consistency
  =============================== */

  if (field.multiple) {
    if (!field.choices && !field.entity) {
      console.warn(
        `Field "${field.name}" is multiple but has no choices or entity`
      )
    }
  }

  /* ===============================
     relation consistency
  =============================== */

  if (field.entity && field.choices) {
    console.warn(
      `Field "${field.name}" has both entity and choices (entity will be ignored)`
    )
  }

  /* ===============================
     html_type consistency
  =============================== */

  if (field.html_type && typeof field.html_type !== "string") {
    throw new Error(
      `Invalid html_type in field "${field.name}"`
    )
  }
}