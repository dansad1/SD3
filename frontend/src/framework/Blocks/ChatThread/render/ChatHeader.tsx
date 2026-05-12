import type {
  ChatParticipant,
  ChatThreadData,
} from "../types"

export function ChatHeader({
  thread,
  participants,
}: {
  thread: ChatThreadData | null
  participants: ChatParticipant[]
}) {
  const others = participants.filter(
    (participant) => !participant.is_self
  )

  const names = others.map((participant) => participant.name)
  const hasOnline = others.some(
    (participant) => participant.online
  )

  const isSingle = others.length === 1

  return (
    <div className="chat-thread__header">
      <div className="chat-thread__header-main">
        <div className="chat-thread__title">
          {thread?.title ||
            (isSingle
              ? names[0]
              : names.join(", ")) ||
            "Диалог"}
        </div>

        <div className="chat-thread__status">
          {isSingle
            ? hasOnline
              ? "в сети"
              : "не в сети"
            : `${others.length} участников`}
        </div>
      </div>
    </div>
  )
}