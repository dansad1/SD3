import { useMemo } from "react"

import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import { resolveRuntimeValue } from "../runtime"

import type {
  ChatMessage,
  ChatParticipant,
  ChatThreadData,
} from "../types"

type InputBlock = {
  participants?: unknown
  messages?: unknown
  thread?: unknown
  currentUserId?: unknown
}

export function useResolvedChatData(block: InputBlock) {
  const runtime = usePageRuntimeContext()

  /* =========================
     👥 PARTICIPANTS
  ========================= */
  const participants = useMemo<ChatParticipant[]>(() => {
    const value = resolveRuntimeValue(
      block.participants,
      runtime
    )

    if (!Array.isArray(value)) {
      return []
    }

    return value.map((item) => {
      const p = item as Record<string, unknown>

      return {
        id: String(p.id ?? ""),
        name: String(p.name ?? ""),
        online: Boolean(p.online),
        is_self: Boolean(p.is_self),
      }
    })
  }, [block.participants, runtime])

  /* =========================
     💬 MESSAGES
  ========================= */
  const messages = useMemo<ChatMessage[]>(() => {
    const value = resolveRuntimeValue(
      block.messages,
      runtime
    )

    if (!Array.isArray(value)) {
      return []
    }

    const mapped = value.map((item) => {
      const m = item as Record<string, unknown>

      return {
        id: String(m.id ?? ""),
        text: String(m.text ?? ""),

        // 🔥 ВСЕГДА string
        author_id: String(m.author_id ?? ""),

        created_at:
          m.created_at != null
            ? String(m.created_at)
            : undefined,

        created_date:
          m.created_date != null
            ? String(m.created_date)
            : undefined,

        timestamp_iso:
          m.timestamp_iso != null
            ? String(m.timestamp_iso)
            : undefined,

        client_id:
          m.client_id != null && m.client_id !== ""
            ? String(m.client_id)
            : undefined,
      }
    })

    // 🔥 стабильная сортировка
    return mapped.sort((a, b) => {
      if (!a.timestamp_iso || !b.timestamp_iso) {
        return 0
      }

      return (
        new Date(a.timestamp_iso).getTime() -
        new Date(b.timestamp_iso).getTime()
      )
    })
  }, [block.messages, runtime])

  /* =========================
     🧵 THREAD
  ========================= */
  const thread = useMemo<ChatThreadData | null>(() => {
    const value = resolveRuntimeValue(
      block.thread,
      runtime
    )

    if (!value || typeof value !== "object") {
      return null
    }

    const t = value as Record<string, unknown>

    return {
      id: t.id != null ? String(t.id) : undefined,
      title:
        t.title != null ? String(t.title) : undefined,
    }
  }, [block.thread, runtime])

  /* =========================
     👤 CURRENT USER
  ========================= */
  const currentUserId = useMemo<string>(() => {
    const value = resolveRuntimeValue(
      block.currentUserId,
      runtime
    )

    return value != null ? String(value) : ""
  }, [block.currentUserId, runtime])

  return {
    participants,
    messages,
    thread,
    currentUserId,
  }
}