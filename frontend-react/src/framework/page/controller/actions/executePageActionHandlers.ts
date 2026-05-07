// page/runtime/actions/executePageActionHandlers.ts

import type { ActionContext } from "@/framework/Blocks/Action/types"
import type {
  PageActionHandler,
  PageRunResult,
} from "../../context/types"

import { validatePageAction } from "./validatePageAction"

export async function executePageActionHandlers(
  actionId: string,
  handlers: PageActionHandler[],
  ctx: ActionContext
): Promise<PageRunResult> {
  for (const handler of handlers) {
    console.log("🔍 PAGE ACTION HANDLER", {
      actionId,
      handlerId: handler.id,
      handler,
      validateSource: handler.validate?.toString?.(),
      runSource: handler.run?.toString?.(),
    })

    const valid = await validatePageAction(
      handler,
      actionId,
      ctx
    )

    if (!valid) {
      console.warn("❌ PAGE ACTION VALIDATION FAILED", {
        actionId,
        handlerId: handler.id,
      })

      return "failed"
    }

    console.log("🚀 PAGE ACTION EXECUTE", {
      actionId,
      handlerId: handler.id,
      ctx,
    })

    const result = await handler.run(ctx)

    console.log("🏁 PAGE ACTION EXECUTE RESULT", {
      actionId,
      handlerId: handler.id,
      result,
    })

    if (result === false) {
      console.warn("❌ PAGE ACTION RETURNED FALSE", {
        actionId,
        handlerId: handler.id,
      })

      return "failed"
    }
  }

  return "handled"
}