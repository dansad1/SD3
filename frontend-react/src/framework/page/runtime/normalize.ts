import { useMemo } from "react"
import { normalizePage } from "@/framework/normalize/normalizePage"
import { traceStep } from "./trace"

import type { ApiPageSchema, ApiPageBlock } from "../PageSchema"

export function useNormalize(
  schema: ApiPageSchema,
  pageId: string
): ApiPageBlock[] {
  return useMemo(() => {
    return traceStep(
      "normalize_blocks",
      pageId,
      { stage: "normalize" },
      () => normalizePage(schema)
    )
  }, [schema, pageId])
}