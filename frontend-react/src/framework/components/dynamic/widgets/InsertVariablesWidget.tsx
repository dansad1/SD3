import type { WidgetProps } from "../types"
import type { FieldSchema } from "../types"

import { BaseWidget } from "./Base"
import Button from "@/framework/components/ui/Button"

/* ================= TYPES ================= */

type VariableItem = {
  key: string
  label?: string
}

type InsertVariablesField = FieldSchema & {
  source?: VariableItem[]
  targetField: string
  format?: "template" | "raw" | "dollar"
}

type InsertCommand = {
  targetField: string
  value: string
  mode: "append" | "replace"
}

/* ================= HELPERS ================= */

function formatValue(
  value: string,
  format: "template" | "raw" | "dollar" = "template"
) {
  if (format === "raw") return value
  if (format === "dollar") return `\${${value}}`
  return `{{ ${value} }}`
}

function isInsertVariablesField(
  field: FieldSchema
): field is InsertVariablesField {
  return field.widget === "InsertVariables"
}

/* ================= COMPONENT ================= */

export function InsertVariablesWidget({
  field,
  onChange,
  loading,
}: WidgetProps) {
  const disabled = Boolean(field.readonly) || Boolean(loading)

  // 🔥 безопасная типизация
  if (!isInsertVariablesField(field)) {
    console.warn(
      "[InsertVariablesWidget] wrong field type",
      field
    )
    return null
  }

  const variables = field.source ?? []
  const targetField = field.targetField
  const format = field.format ?? "template"

  if (!targetField) return null

  const handleInsert = (item: VariableItem) => {
    if (disabled) return

    const value = formatValue(item.key, format)

    const command: InsertCommand = {
      targetField,
      value,
      mode: "append",
    }

    onChange(command)
  }

  return (
    <BaseWidget field={field} loading={loading}>
      <div className="flex flex-wrap gap-2">
        {variables.map((v) => (
          <Button
            key={v.key}
            type="button"
            size="sm"
            disabled={disabled}
            onClick={() => handleInsert(v)}
          >
            {v.label ?? v.key}
          </Button>
        ))}
      </div>
    </BaseWidget>
  )
}