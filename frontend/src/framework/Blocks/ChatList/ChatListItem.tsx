// src/framework/Blocks/Chat/render/ChatListItem.tsx

import type { ChatListItem } from "./types"

export function ChatListItemView({
  item,
  selected,
  onClick,
  showTimestamp,
  showUnread,
}: {
  item: ChatListItem
  selected: boolean
  onClick: () => void
  showTimestamp?: boolean
  showUnread?: boolean
}) {
  const unread = item.unread ?? 0
  const isUnread = unread > 0

  return (
    <div
      className={[
        "chat-list__item",
        selected && "chat-list__item--selected",
        isUnread && "chat-list__item--unread",
      ]
        .filter(Boolean)
        .join(" ")}
      onClick={onClick}
    >
      {/* CONTENT */}
      <div className="chat-list__content">

        {/* TOP ROW */}
        <div className="chat-list__row">
          <div className="chat-list__title">
            {item.title}
          </div>

          {showTimestamp && item.timestamp && (
            <div className="chat-list__time">
              {formatTime(item.timestamp)}
            </div>
          )}
        </div>

        {/* SUBTITLE */}
        <div className="chat-list__subtitle">
          {item.subtitle}
        </div>
      </div>

      {/* META */}
      <div className="chat-list__meta">
        {showUnread && isUnread && (
          <div className="chat-list__badge">
            {unread}
          </div>
        )}
      </div>
    </div>
  )
}

/* ========================= */

function formatTime(ts: string) {
  const date = new Date(ts)
  const now = new Date()

  const isToday =
    date.toDateString() === now.toDateString()

  if (isToday) {
    return date.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return date.toLocaleDateString()
}