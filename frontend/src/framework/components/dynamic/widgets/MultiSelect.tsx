import PopupMultiSelect from "../../ui/PopupMultiSelect"
import type { Value, WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

/* =========================
   TYPES
========================= */

type Primitive = string | number

type RelationObject = {
  value?: Primitive
  id?: Primitive
  label?: string
}



/* =========================
   HELPERS
========================= */

function toId(v: unknown): string {
  if (typeof v === "object" && v !== null) {
    const obj = v as RelationObject
    const id = obj.value ?? obj.id

    return id !== undefined
      ? String(id)
      : ""
  }

  if (
    typeof v === "string" ||
    typeof v === "number"
  ) {
    return String(v)
  }

  return ""
}

function normalizeArray(
  v: Value
): string[] {

  if (!Array.isArray(v)) {
    return []
  }

  return v
    .map(toId)
    .filter(Boolean)
}

/* =========================
   COMPONENT
========================= */

export const MultiSelectWidget:
WidgetRenderer = (
  props
) => {

  const {
    field,
    value,
    onChange,
    loading,
  } = props

  const normalizedValue =
    normalizeArray(value)

  const options =
    field.options ?? []

  console.log(
    "MULTISELECT",
    {
      name: field.name,
      value,
      normalizedValue,
      options:
        options.length,
    }
  )

  return (
    <BaseWidget
      field={field}
      loading={loading}
    >

      {({ disabled }) => (

        <PopupMultiSelect

          value={
            normalizedValue
          }

          options={
            options
          }

          onChange={(
            ids: string[]
          ) => {

            onChange(ids)

          }}

          disabled={
            disabled
          }

        />

      )}

    </BaseWidget>
  )
}