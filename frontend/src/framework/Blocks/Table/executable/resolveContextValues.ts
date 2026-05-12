// table/runtime/executable/resolveContextValues.ts

import { resolveRowId } from "./resolveRowId"
import { getByPath } from "./getByPath"
import type { BaseRow } from "../types/runtime"

type ContextValue =
  | string
  | number
  | boolean
  | null
  | undefined
  | object

type ContextInput = Record<string, ContextValue>
type ContextOutput = Record<string, ContextValue>

export function resolveContextValues<
  T extends BaseRow
>(
  input: ContextInput | undefined,
  row: T
): ContextOutput {
  if (!input) {
    return {}
  }

  const rowId = resolveRowId(row)

  const result: ContextOutput = {}

  for (const key in input) {
    const value = input[key]

    if (typeof value === "string") {
      if (value.startsWith("$row.")) {
        const field = value.replace(
          "$row.",
          ""
        )

        result[key] = getByPath(
          row as Record<string, unknown>,
          field
        ) as ContextValue

        continue
      }

      if (
        value.startsWith("$selection.")
      ) {
        const field = value.replace(
          "$selection.",
          "selection."
        )

        result[key] = getByPath(
          row as Record<string, unknown>,
          field
        ) as ContextValue

        continue
      }

      if (value === "$id") {
        result[key] = rowId
        continue
      }
    }

    result[key] = value
  }

  return result
}