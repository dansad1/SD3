import type { Json } from "@/framework/types/json"
import type { ActionResult } from "./types"
import { buildFinalContext } from "./buildFinalContext"
import { withTrace } from "./withTrace"
import { api } from "../client"

export function submitAction(
  code: string,
  data: Record<string, Json> = {},
  ctx?: Record<string, Json>
): Promise<ActionResult> {

  if (typeof code !== "string") {
    console.error("❌ INVALID ACTION CODE:", code)
    throw new Error("Action code must be string")
  }

  const finalCtx = buildFinalContext(ctx)

  const payload = {
    ...data,
    _ctx: finalCtx,
  }

  console.log("📤 ACTION SUBMIT", { code, payload })

  const exec = () =>
    api.post(
  `/action/${code}/submit/`,
  payload
    )

  return withTrace("action_submit", exec, {
    stage: "action_submit",
    action: code,
    block: "Action",
    payloadKeys: Object.keys(data).length,
    hasCtx: Object.keys(finalCtx).length > 0,
  })
}