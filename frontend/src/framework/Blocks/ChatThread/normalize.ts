// src/framework/normalize/normalizeContent.ts

import { normalizeId } from "@/framework/normalize/normalizeCommon"

import type { ApiPageBlock } from "@/framework/page/PageSchema"

type ChatThreadApi = Extract<
  ApiPageBlock,
  { type: "chat_thread" }
>

export function normalizeChatThread(
  block: ChatThreadApi
): ChatThreadApi {
  return {
    ...block,
    id: normalizeId(block.id),

    participants: block.participants ?? [],
    messages: block.messages ?? [],

    features: {
      header:
        block.features?.header ?? true,

      participants:
        block.features?.participants ?? true,

      timestamps:
        block.features?.timestamps ?? true,

      grouping:
        block.features?.grouping ?? true,

      autoScroll:
        block.features?.autoScroll ?? true,

      realtime:
        block.features?.realtime ?? false,

      attachments:
        block.features?.attachments ?? false,
    },
  }
}