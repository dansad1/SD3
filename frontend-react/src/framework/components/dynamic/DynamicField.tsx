import { widgetRegistry } from "./registry"
import type { FieldSchema, Value } from "./types"
import FallbackWidget from "./widgets/Fallback"

interface Props {
  field: FieldSchema
  value: Value
  onChange: (value: Value) => void
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

  const Widget = widgetRegistry[field.widget] ?? FallbackWidget

  if (!widgetRegistry[field.widget]) {
    console.warn(
      `[DynamicField] Unknown widget "${field.widget}"`,
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