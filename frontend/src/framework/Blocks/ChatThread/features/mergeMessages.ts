import type { ChatMessage } from "../types"

function getSortValue(message: ChatMessage, index: number): string {
  if (message.timestamp_iso) {
    return `${message.timestamp_iso}__${index}`
  }

  if (message.optimistic) {
    return `zzzz__${index}`
  }

  return `yyyy__${index}`
}

export function mergeMessages(
  serverMessages: ChatMessage[],
  optimisticMessages: ChatMessage[]
): ChatMessage[] {
  const byClientId = new Set(
    serverMessages
      .map((m) => m.client_id)
      .filter((v): v is string => Boolean(v))
  )

  const filteredOptimistic = optimisticMessages.filter((m) => {
    if (!m.client_id) {
      return true
    }

    return !byClientId.has(m.client_id)
  })

  const merged = [...serverMessages, ...filteredOptimistic]

  merged.sort((a, b) => {
    const ia = merged.indexOf(a)
    const ib = merged.indexOf(b)

    return getSortValue(a, ia).localeCompare(
      getSortValue(b, ib)
    )
  })

  return merged
}