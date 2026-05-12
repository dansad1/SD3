import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type Api = Extract<ApiPageBlock, { type: "document" }>

export function normalizeDocument(block: Api): Api {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}
