// page/runtime/actions/runPageAction.ts

import type { ActionContext } from "@/framework/Blocks/Action/types"
import type {
  ActionRuntime,
  PageRunResult,
} from "../../context/types"

import { sortHandlers } from "./sortHandlers"
import { executePageActionHandlers } from "./executePageActionHandlers"

export async function runPageAction(
  runtime: Record<string, ActionRuntime>,
  actionId: string,
  ctx: ActionContext = {}
): Promise<PageRunResult> {
  console.log("🏃 PAGE ACTION RUN REQUEST", {
    actionId,
    ctx,
    runtime,
    runtimeKeys: Object.keys(runtime),
  })

  const bucket = runtime[actionId]

  console.log("📦 PAGE ACTION BUCKET", {
    actionId,
    bucket,
  })

  if (!bucket) {
    console.warn("⚠️ PAGE ACTION NOT FOUND", {
      actionId,
      available: Object.keys(runtime),
    })

    return "not_found"
  }

  const handlers = sortHandlers(bucket.handlers)

  console.log("📚 PAGE ACTION HANDLERS", {
    actionId,
    handlers,
  })

  const result = await executePageActionHandlers(
    actionId,
    handlers,
    ctx
  )

  console.log("🏁 PAGE ACTION FINAL RESULT", {
    actionId,
    result,
  })

  return result
}