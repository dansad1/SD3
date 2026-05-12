import type { ChatMessage } from "../types"

type Props = {
  messages: ChatMessage[]
  currentUserId: string
  grouping?: boolean
  timestamps?: boolean
}

export function ChatMessages({
  messages,
  currentUserId,
  grouping,
  timestamps,
}: Props) {
  return (
    <>
      {messages.map((m, i) => {
        const prev = messages[i - 1]

        // 🔥 фикс
        const own =
          currentUserId !== "" &&
          m.author_id !== "" &&
          String(m.author_id) ===
            String(currentUserId)

            const GROUP_TIMEOUT = 5 * 60 * 1000 // 5 минут

        const isGrouped = Boolean(
  grouping &&
    prev &&
    String(prev.author_id) === String(m.author_id) &&
    prev.created_date === m.created_date &&
    prev.timestamp_iso &&
    m.timestamp_iso &&
    new Date(m.timestamp_iso).getTime() -
      new Date(prev.timestamp_iso).getTime() <
      GROUP_TIMEOUT
)

        const showDate = Boolean(
          m.created_date &&
            (!prev ||
              prev.created_date !==
                m.created_date)
        )

        return (
          <div key={String(m.client_id || m.id)}>
            {showDate && (
              <div className="chat-thread__date-group">
                <div className="chat-thread__date-label">
                  {m.created_date}
                </div>
              </div>
            )}

            <div
              className={[
                "chat-thread__message",
                own && "chat-thread__message--own",
                isGrouped &&
                  "chat-thread__message--grouped",
              ]
                .filter(Boolean)
                .join(" ")}
            >
              <div className="chat-thread__bubble">
                <div
                  className="chat-thread__text"
                  dangerouslySetInnerHTML={{
                    __html: m.text,
                  }}
                />

                {timestamps && m.created_at && (
                  <div className="chat-thread__time">
                    {m.created_at}
                  </div>
                )}
              </div>
            </div>
          </div>
        )
      })}
    </>
  )
}