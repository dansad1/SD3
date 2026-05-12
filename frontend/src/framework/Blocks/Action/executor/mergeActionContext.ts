// mergeActionContext.ts

import type { ActionContext } from "@/framework/Blocks/Action/types"

export function mergeActionContext(
  runtimeContext: ActionContext,
  ctx: ActionContext
): ActionContext {
  const merged: ActionContext = {
    ...runtimeContext,
    ...ctx,

    page: {
      ...runtimeContext.page,
      ...ctx.page,

      params: {
        ...runtimeContext.page?.params,
        ...ctx.page?.params,
      },

      query: {
        ...runtimeContext.page?.query,
        ...ctx.page?.query,
      },
    },

    data: {
      ...(runtimeContext.data ?? {}),
      ...(ctx.data ?? {}),
    },
  }

  console.log("🧩 mergeActionContext", {
    runtimeContext,
    ctx,
    merged,
  })

  return merged
}