import type { BaseBlock } from "../BlockType"

export type ChatListBlock = BaseBlock & {
  type: "chat_list"

  data?: unknown

  selectedId?: string

  to: string

  features?: {
    unread?: boolean
    timestamp?: boolean
  }
}
export type ChatListItem = {
  id: string | number

  title: string

  // 🔥 ВАЖНО — то что приходит с бэка
  subtitle?: string

  timestamp?: string

  unread?: number

  online?: boolean

  type?: "chat" | "broadcast" | "broadcast_sent"
}
