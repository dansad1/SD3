// TableCell.tsx
import React from "react"
import type {
  BaseRow,
  ListFieldMeta,
} from "@/framework/Blocks/Table/types/runtime"
import type { Json } from "@/framework/types/json"

type Props<T extends BaseRow> = {
  field: ListFieldMeta
  row: T
}

function renderValue(value: Json) {
  if (value === null || value === undefined) return ""

  if (React.isValidElement(value)) return value

  if (typeof value === "object") {
    if (Array.isArray(value)) {
      return value
        .map((item) => {
          if (
            item &&
            typeof item === "object" &&
            "label" in item
          ) {
            return String((item as { label: unknown }).label)
          }

          return String(item)
        })
        .join(", ")
    }

    if ("label" in value) {
      return String((value as { label: unknown }).label)
    }

    try {
      return JSON.stringify(value)
    } catch {
      return "[Object]"
    }
  }

  return String(value)
}

export function TableCell<T extends BaseRow>({
  field,
  row,
}: Props<T>) {
  return (
    <>
      {renderValue(row[field.key])}
    </>
  )
}