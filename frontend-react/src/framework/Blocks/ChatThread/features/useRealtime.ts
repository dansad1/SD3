// src/framework/Blocks/Chat/features/useRealtime.ts

import { useEffect } from "react"

export function useRealtime(
  enabled: boolean | undefined,
  chatId: string | undefined
) {
  useEffect(() => {
    if (!enabled) {
      return
    }

    const interval = window.setInterval(() => {
      console.log(
        "[chat_thread] realtime refresh:",
        chatId
      )
    }, 5000)

    return () => {
      window.clearInterval(interval)
    }
  }, [enabled, chatId])
}