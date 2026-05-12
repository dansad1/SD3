import { useState } from "react"

import type { Json } from "@/framework/types/json"
import type { ChatMessage } from "../types"

import { submitAction } from "@/framework/api/action/submitAction"

export function useChatSend(
  action: string,
  ctx: Record<string, unknown> | undefined,
  currentUserId: string,
  addOptimistic: (msg: ChatMessage) => void
) {
  const [value, setValue] = useState("")
  const [loading, setLoading] = useState(false)

  const send = async () => {
    const text = value.trim()

    if (!text) return

    const now = new Date()

    const clientId = `tmp-${Date.now()}-${Math.random()
      .toString(36)
      .slice(2, 8)}`

    const optimisticMessage: ChatMessage = {
      id: clientId,
      client_id: clientId,
      text,

      // 🔥 важно
      author_id: currentUserId || "temp-user",

      created_at: now.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),

      created_date: now.toISOString().slice(0, 10),
      timestamp_iso: now.toISOString(),

      optimistic: true,
      status: "sending",
    }

    addOptimistic(optimisticMessage)

    setValue("")
    setLoading(true)

    try {
      await submitAction(
        action,
        {
          body: text,
          client_id: clientId,
        },
        ctx as Record<string, Json> | undefined
      )
    } catch  {
      // 🔴 помечаем ошибку
      addOptimistic({
        ...optimisticMessage,
        status: "error",
      })
    } finally {
      setLoading(false)
    }
  }

  return {
    value,
    setValue,
    send,
    loading,
  }
}