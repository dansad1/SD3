import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type Api = Extract<ApiPageBlock, { type: "menu" }>

export function normalizeMenu(block: Api): Api {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}
