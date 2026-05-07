// src/framework/Blocks/Chat/types.ts

import type { BaseBlock } from "../BlockType"

/* ================= PARTICIPANTS ================= */

export type ChatParticipant = {
  id: string
  name: string
  online?: boolean
  is_self?: boolean
}

/* ================= ATTACHMENTS ================= */

export type ChatAttachment = {
  id: string
  name: string
  url: string
}

/* ================= MESSAGE ================= */

export type ChatMessage = {
  id: string | number
  text: string
  author_id: string

  created_at?: string
  created_date?: string
  timestamp_iso?: string

  attachments?: ChatAttachment[]
  client_id?: string

  // 🔥 ДОБАВЬ ЭТО
  optimistic?: boolean
  status?: "sending" | "sent" | "error"
}
/* ================= THREAD ================= */

export type ChatThreadData = {
  id?: string
  title?: string
}

/* ================= BLOCK ================= */

export type ChatThreadBlock = BaseBlock & {
  type: "chat_thread"

  thread?: unknown
  participants?: unknown[]
  messages?: unknown[]

  // 🔥 всегда строка после нормализации
  currentUserId?: string

  reply?: {
    schema: string

    submit: {
      action: string
      label?: string

      redirect?:
        | string
        | {
            to: string
            ctx?: Record<string, unknown>
          }

      closeModal?: boolean
    }

    ctx?: Record<string, unknown>
  }

  features?: {
    header?: boolean
    participants?: boolean
    timestamps?: boolean
    grouping?: boolean
    autoScroll?: boolean
    realtime?: boolean
    attachments?: boolean
  }
}