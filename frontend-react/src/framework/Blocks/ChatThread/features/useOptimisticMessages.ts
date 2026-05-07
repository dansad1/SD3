import { useCallback, useState } from "react"

import type { ChatMessage } from "../types"

export function useOptimisticMessages() {
  const [optimistic, setOptimistic] = useState<ChatMessage[]>([])

  const addMessage = useCallback((msg: ChatMessage) => {
    setOptimistic((prev) => [...prev, msg])
  }, [])

  const markResolvedByServer = useCallback(
    (serverMessages: ChatMessage[]) => {
      const serverClientIds = new Set(
        serverMessages
          .map((m) => m.client_id)
          .filter((v): v is string => Boolean(v))
      )

      setOptimistic((prev) =>
        prev.filter((m) => {
          if (!m.client_id) {
            return true
          }

          return !serverClientIds.has(m.client_id)
        })
      )
    },
    []
  )

  return {
    optimistic,
    addMessage,
    markResolvedByServer,
  }
}