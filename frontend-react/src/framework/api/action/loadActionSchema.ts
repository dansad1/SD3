// src/framework/api/action/loadActionSchema.ts

import type { Json } from "@/framework/types/json"
import { buildFinalContext } from "./buildFinalContext"
import type { ApiFormSchema } from "../form/types"
import { withTrace } from "./withTrace"
import { api } from "../client"

export function loadActionSchema(
  code: string,
  ctx?: Record<string, Json>
): Promise<ApiFormSchema> {
  const finalCtx = buildFinalContext(ctx)

  const params = new URLSearchParams()
  if (Object.keys(finalCtx).length > 0) {
    params.set("ctx", JSON.stringify(finalCtx))
  }

  const query = params.toString()
  const url = `/action/${code}/form/${query ? `?${query}` : ""}`

  const exec = () => api.get<ApiFormSchema>(url)

  return withTrace("action_schema_load", exec, {
    stage: "action_schema_load",
    action: code,
    block: "ActionForm",
    hasCtx: Object.keys(finalCtx).length > 0,
    ctxKeys: Object.keys(finalCtx).length,
  })
}