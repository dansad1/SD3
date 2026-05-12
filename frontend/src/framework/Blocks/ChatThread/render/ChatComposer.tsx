import { useMemo } from "react"

import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"

import { useChatSend } from "../features/useChatSend"
import { resolveRuntimeValue } from "../runtime"

import type { ChatMessage } from "../types"

type Props = {
  action: string
  ctx?: Record<string, unknown>
  currentUserId: string
  addOptimistic: (msg: ChatMessage) => void
}

export function ChatComposer({
  action,
  ctx,
  currentUserId,
  addOptimistic,
}: Props) {
  const runtime = usePageRuntimeContext()

  const resolvedCtx = useMemo(() => {
    if (!ctx) {
      return {}
    }

    const result: Record<string, unknown> = {}

    for (const key of Object.keys(ctx)) {
      result[key] = resolveRuntimeValue(
        ctx[key],
        runtime
      )
    }

    return result
  }, [ctx, runtime])

  const {
    value,
    setValue,
    send,
    loading,
  } = useChatSend(
    action,
    resolvedCtx,
    currentUserId,
    addOptimistic
  )

  return (
    <div className="chat-thread__composer">
      <textarea
        className="chat-thread__textarea"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Введите сообщение..."
        rows={2}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            void send()
          }
        }}
      />

      <button
        className="chat-thread__send"
        onClick={() => {
          void send()
        }}
        disabled={loading || !value.trim()}
      >
        {loading ? "..." : "Отправить"}
      </button>
    </div>
  )
}