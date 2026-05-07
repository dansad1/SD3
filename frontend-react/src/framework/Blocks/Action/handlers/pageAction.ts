// framework/action/handlers/pageAction.ts

import type { PageApi } from "@/framework/page/context/types"
import type { ActionContext } from "../types"

export async function runPageAction(
  page: PageApi,
  actionId: string,
  ctx: ActionContext
): Promise<"handled" | "not_found" | "failed"> {

  return page.run(actionId, ctx)
}