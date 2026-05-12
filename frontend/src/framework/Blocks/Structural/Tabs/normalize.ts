import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type TabsApi = Extract<ApiPageBlock, { type: "tabs" }>

export function normalizeTabs(
  block: TabsApi
): TabsApi {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}
