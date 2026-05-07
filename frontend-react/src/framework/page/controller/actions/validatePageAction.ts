// page/runtime/actions/validatePageAction.ts

import type {
  PageActionHandler,
} from "../../context/types"
import type { ActionContext } from "@/framework/Blocks/Action/types"

export async function validatePageAction(
  handler: PageActionHandler,
  actionId: string,
  ctx: ActionContext
): Promise<boolean> {
  if (!handler.validate) {
    return true
  }

  console.log("🧪 HANDLER VALIDATE SOURCE", {
    actionId,
    handlerId: handler.id,
    validate: handler.validate.toString(),
  })

  const valid = await handler.validate(ctx)

  console.log("🧪 PAGE ACTION VALIDATE", {
    actionId,
    handlerId: handler.id,
    valid,
  })

  return valid
}