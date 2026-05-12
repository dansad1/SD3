// src/framework/api/form/buildFormParams.ts

import type { Json } from "@/framework/types/json"

export function buildFormParams(
  mode: "create" | "edit" = "create",
  objectId?: string | number,
  initial?: Record<string, Json>
) {
  const params = new URLSearchParams()

  params.set("mode", mode)

  if (mode === "edit" && objectId !== undefined) {
    params.set("id", String(objectId))
  }

  if (initial && Object.keys(initial).length > 0) {
    params.set("initial", JSON.stringify(initial))
  }

  return params.toString()
}