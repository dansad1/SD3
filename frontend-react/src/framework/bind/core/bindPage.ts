// src/framework/bind/core/bindPage.ts

import type {
  PageRuntimeContext,
  AnyBlock,
} from "../types"
import { buildBindScope } from "../scope/bindScope"
import { bindBlock } from "./bindBlock"
import { traceRuntime } from "@/framework/trace/runtime"

export function bindPage<T extends AnyBlock>(
  blocks: T[],
  ctx: PageRuntimeContext
): T[] {
  const trace = traceRuntime.current()

  const runBind = () => {
    const scope = buildBindScope(ctx)

    return blocks.flatMap((b) => {
      const result = bindBlock(b, scope)
      if (!result) return []
      return Array.isArray(result) ? result : [result]
    }) as T[]
  }

  if (!trace) return runBind()

  const result = trace.stepSync(
    "bind_page",
    runBind,
    {
      stage: "bind",
      pageCtxKeys: Object.keys(ctx ?? {}).length,
      blocksBefore: blocks.length,
    }
  )

  trace.annotate({
    blocksAfter: result.length,
    before: blocks,
    after: result,
    changed: blocks !== result,
  })

  return result
}