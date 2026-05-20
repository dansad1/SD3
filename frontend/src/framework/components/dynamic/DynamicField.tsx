import {
  widgetRegistry,
} from "./registry"

import type {
  FieldSchema,
  Value,
} from "./types"

import FallbackWidget from "./widgets/Fallback"

import {
  resolveFieldWidget,
} from "./resolveFieldWidget"

interface Props {

  field: FieldSchema

  value: Value

  onChange: (
    value: Value
  ) => void

  loading?: boolean
}

export default function DynamicField({
  field,
  value,
  onChange,
  loading,
}: Props) {

  /* ===============================
     Widget resolve
  =============================== */

  const widgetKey =
    resolveFieldWidget(
      field,
      "form",
      "desktop",
    )

  const Widget =
    widgetRegistry[
      widgetKey
    ]?.component
    ?? FallbackWidget

  if (
    !widgetRegistry[
      widgetKey
    ]
  ) {

    console.warn(
      `[DynamicField] Unknown widget "${widgetKey}"`,
      field
    )
  }

  /* ===============================
     Render
  =============================== */

  return (
    <Widget
      field={field}
      value={value}
      onChange={onChange}
      loading={loading}
    />
  )
}