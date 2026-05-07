import type { ChatMessage } from "../types"

export function ChatMessageItem({
  message,
  own,
  timestamps,
  attachments,
  isGrouped,
}: {
  message: ChatMessage
  own: boolean
  timestamps?: boolean
  attachments?: boolean
  isGrouped?: boolean
}) {
  return (
    <div
      className={[
        "chat-thread__message",
        own && "chat-thread__message--own",
        isGrouped && "chat-thread__message--grouped",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <div className="chat-thread__bubble">
        {/* текст */}
        <div className="chat-thread__text">
          {message.text}
        </div>

        {/* файлы */}
        {attachments &&
          message.attachments?.length ? (
            <div className="chat-thread__attachments">
              {message.attachments.map((file) => (
                <a
                  key={file.id}
                  href={file.url}
                  className="chat-thread__attachment"
                  target="_blank"
                  rel="noreferrer"
                >
                  {file.name}
                </a>
              ))}
            </div>
          ) : null}

        {/* время */}
        {timestamps && message.created_at && (
          <div className="chat-thread__time">
            {message.created_at}
          </div>
        )}
      </div>
    </div>
  )
}