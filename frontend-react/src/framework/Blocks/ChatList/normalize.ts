import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type ChatListApi = Extract<ApiPageBlock, { type: "chat_list" }>

export function normalizeChatList(
  block: ChatListApi
): ChatListApi {
  return {
    ...block,
    id: normalizeId(block.id),
    features: {
      unread: true,
      timestamp: true,
      ...block.features,
    },
  }
}
