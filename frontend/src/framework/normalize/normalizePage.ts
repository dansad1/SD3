// src/framework/normalize/normalizePage.ts

import type {
  ApiPageSchema,
  PageBlock,
} from "../page/PageSchema"

import { dispatchNormalize } from "./normalizeDispatch"
import { traceRuntime } from "@/framework/trace/runtime"

/* =========================================================
   NORMALIZE PAGE
========================================================= */

export function normalizePage(
  schema: ApiPageSchema
): PageBlock[] {

  const trace = traceRuntime.current()

  const runNormalize = () => {
    return schema.blocks.map(dispatchNormalize)
  }

  if (!trace) {
    return runNormalize()
  }

  const beforeSnapshot = schema.blocks

  const result = trace.stepSync(
    "normalize_page",
    runNormalize,
    {
      stage: "normalize",
      pageTitle: schema.title,
      blocksBefore: beforeSnapshot?.length ?? 0,
      blockTypesBefore: beforeSnapshot?.map(b => b.type),
    }
  )

  trace.annotate({
    blocksAfter: result.length,
    changed: beforeSnapshot !== result,
    before: beforeSnapshot,
    after: result,
  })

  return result
}