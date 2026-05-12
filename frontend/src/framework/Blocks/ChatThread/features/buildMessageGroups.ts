// src/framework/Blocks/Chat/features/buildMessageGroups.ts

import type { ChatMessage } from "../types"

export type ChatMessageGroup = {
  date?: string
  messages: ChatMessage[]
}

export function buildMessageGroups(
  messages: ChatMessage[],
  enabled: boolean | undefined
): ChatMessageGroup[] {
  if (!enabled) {
    return [
      {
        messages,
      },
    ]
  }

  const groups: ChatMessageGroup[] = []

  for (const message of messages) {
    const date = message.created_date ?? ""

    const last = groups[groups.length - 1]

    if (!last || last.date !== date) {
      groups.push({
        date,
        messages: [message],
      })

      continue
    }

    last.messages.push(message)
  }

  return groups
}