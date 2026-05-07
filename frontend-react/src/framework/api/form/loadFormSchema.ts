// src/framework/api/form/loadFormSchema.ts

import { traceRuntime } from "@/framework/trace/runtime"
import type { ApiFormSchema } from "./types"
import { api } from "../client"

export function loadFormSchema(
  entity: string,
  mode: "create" | "edit" = "create",
  objectId?: string | number,
  query?: Record<string, unknown>
): Promise<ApiFormSchema> {

  const params = new URLSearchParams()

  // 🔥 прокидываем runtime query (а не window!)
  if (query) {
    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.set(key, String(value))
      }
    })
  }

  // системные параметры
  params.set("mode", mode)

  if (mode === "edit" && objectId !== undefined) {
    params.set("id", String(objectId))
  }

  const url = `/entity/${entity}/form/?${params.toString()}`

  const exec = () => api.get<ApiFormSchema>(url)
  const trace = traceRuntime.current()

  if (!trace) {
    return exec()
  }

  return trace.step(
    "form_schema_load",
    exec,
    {
      block: "Form",
      entity,
      mode,
      objectId,
      queryKeys: query ? Object.keys(query) : [],
    }
  )
}