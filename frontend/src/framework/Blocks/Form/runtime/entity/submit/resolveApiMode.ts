// form/hooks/submit/resolveApiMode.ts

import type { EntityFormMode } from "../../../types/runtime";


export function resolveApiMode(
  mode?: EntityFormMode
): "create" | "edit" {
  return mode === "edit" || mode === "view"
    ? "edit"
    : "create"
}