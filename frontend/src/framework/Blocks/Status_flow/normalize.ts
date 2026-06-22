import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type Api = Extract<ApiPageBlock, { type: "status_flow" }>

export function normalizeStatus_flow(block: Api): Api {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}
