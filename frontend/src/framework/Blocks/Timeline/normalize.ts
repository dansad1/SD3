import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type Api = Extract<ApiPageBlock, { type: "timeline" }>

export function normalizeTimeline(block: Api): Api {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}
