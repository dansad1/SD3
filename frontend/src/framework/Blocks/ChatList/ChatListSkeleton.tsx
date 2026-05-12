export function ChatListSkeleton() {
  return (
    <div className="chat-list">
      {Array.from({ length: 6 }).map((_, i) => (
        <div key={i} className="chat-list__item skeleton">
          <div className="skeleton-avatar" />
          <div className="skeleton-lines">
            <div className="skeleton-line short" />
            <div className="skeleton-line" />
          </div>
        </div>
      ))}
    </div>
  )
}