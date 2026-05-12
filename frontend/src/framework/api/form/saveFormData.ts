// src/framework/api/form/saveFormData.ts
import { traceRuntime } from "@/framework/trace/runtime"
import type { Json } from "@/framework/types/json"
import { api } from "../client"
import { buildFormParams } from "./buildFormParams"
import type { PageEffect } from "@/framework/page/runtime/effects/types"

export type RedirectTarget =
  | string
  | {
      to: string
      ctx?: Record<string, unknown>
    }

export type FormSubmitResult = {
  status: "ok" | "error"
  message?: string
  errors?: Record<string, string[]>
  redirect?: RedirectTarget
  effects?: PageEffect[]
  id?: string | number
  [key: string]: unknown
}
export function saveFormData(
  entity: string,
  data: Record<string, Json>,
  mode: "create" | "edit" = "create",
  objectId?: string | number
): Promise<FormSubmitResult> {
  const query = buildFormParams(mode, objectId)
  const url = `/entity/${entity}/form/submit/?${query}`

  const exec = () =>
    api.post<FormSubmitResult>(url, data)

  const trace = traceRuntime.current()

  if (!trace) {
    return exec()
  }

  return trace.step(
    "form_submit",
    exec,
    {
      block: "Form",
      entity,
      mode,
      objectId,
      payloadKeys: Object.keys(data).length,
    }
  )
}