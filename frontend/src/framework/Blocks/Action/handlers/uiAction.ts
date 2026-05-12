// src/framework/action/handlers/uiAction.ts

import { actionRegistry } from "../registry"
import type { ActionContext } from "../types"

export async function runUIAction(
  actionId: string,
  ctx: ActionContext
): Promise<boolean> {
  console.log("🖥 UI ACTION LOOKUP", {
    actionId,
    available: actionRegistry.all().map(x => x.id),
  })

  const handler = actionRegistry.get(actionId)

  console.log("🖥 UI ACTION HANDLER", {
    actionId,
    handler,
  })

  if (!handler) {
    console.warn("❌ UI ACTION NOT FOUND", actionId)
    return false
  }

  try {
    const result = await handler.run(ctx)

    console.log("🖥 UI ACTION HANDLER RESULT", {
      actionId,
      result,
    })

    return result !== false
  } catch (e) {
    console.error("❌ UI ACTION ERROR", {
      actionId,
      error: e,
    })

    return false
  }
}