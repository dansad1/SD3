import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type Api = Extract<ApiPageBlock, { type: "custom" }>

export function normalizeCustom(block: Api): Api {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}
