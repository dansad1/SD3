import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type Api = Extract<ApiPageBlock, { type: "accordion" }>

export function normalizeAccordion(block: Api): Api {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}
