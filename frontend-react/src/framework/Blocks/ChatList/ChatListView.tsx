// src/framework/Blocks/Chat/render/ChatListView.tsx

import { ChatListItemView } from "./ChatListItem"
import type { ChatListItem } from "./types"

export function ChatListView({
  items,
  selectedId,
  onOpen,
  features,
}: {
  items: ChatListItem[]
  selectedId: string
  onOpen: (id: string | number) => void
  features?: {
    unread?: boolean
    timestamp?: boolean
  }
}) {
  return (
    <div className="chat-list">
      {items.map((item) => (
        <ChatListItemView
          key={item.id}
          item={item}
          selected={String(item.id) === selectedId}
          onClick={() => onOpen(item.id)}
          showTimestamp={features?.timestamp}
          showUnread={features?.unread}
        />
      ))}
    </div>
  )
}