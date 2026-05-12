export function ChatThreadSkeleton() {
  return (
    <div className="chat-thread__messages">
      {Array.from({ length: 8 }).map((_, i) => (
        <div
          key={i}
          className={`chat-thread__message ${
            i % 2 ? "chat-thread__message--own" : ""
          }`}
        >
          <div className="chat-thread__bubble skeleton-line" />
        </div>
      ))}
    </div>
  )
}