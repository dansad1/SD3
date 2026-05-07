// table/runtime/executable/resolveRowId.ts

import type { BaseRow } from "../types/runtime"


export function resolveRowId(
  row: BaseRow
): string | number | undefined {
  if (
    typeof row.id === "string" ||
    typeof row.id === "number"
  ) {
    return row.id
  }

  if (
    typeof row.pk === "string" ||
    typeof row.pk === "number"
  ) {
    return row.pk
  }

  if (
    typeof row.uuid === "string" ||
    typeof row.uuid === "number"
  ) {
    return row.uuid
  }

  return undefined
}