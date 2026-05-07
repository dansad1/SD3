import { useMemo } from "react"
import { bindPage } from "@/framework/bind/core/bindPage"
import { traceStep } from "./trace"

import type { ApiPageBlock } from "../PageSchema"
import type { PageRuntimeContext } from "@/framework/bind/types"

export function useBind(
  blocks: ApiPageBlock[],
  ctx: PageRuntimeContext,
  pageId: string
): ApiPageBlock[] {
  console.log("CTX REF CHANGED?", ctx)
  console.log("CTX:", ctx.query)
  return useMemo(() => {
    return traceStep(
      "bind_blocks",
      pageId,
      { stage: "bind" },
      () => bindPage(blocks, ctx)
    )
  }, [blocks, ctx, pageId])
}