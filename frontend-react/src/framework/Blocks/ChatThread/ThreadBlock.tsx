// src/framework/Blocks/Chat/ChatThreadBlock.tsx

import { useEffect, useMemo, useRef } from "react"

import type { BlockComponent } from "../Registry/BlockRegistry"

import { useResolvedChatData } from "./features/useResolvedChatData"
import { useOptimisticMessages } from "./features/useOptimisticMessages"
import { useAutoScroll } from "./features/useAutoScroll"
import { useRealtime } from "./features/useRealtime"
import { mergeMessages } from "./features/mergeMessages"

import { ChatMessages } from "./render/ChatMessages"
import { ChatHeader } from "./render/ChatHeader"
import { ChatComposer } from "./render/ChatComposer"
import { ChatThreadSkeleton } from "./render/ChatThreadSkeleton"
import { ChatThreadEmpty } from "./render/ChatThreadEmpty"

export const ChatThreadBlock: BlockComponent<"chat_thread"> = ({
  block,
}) => {
  const {
    participants,
    messages,
    thread,
    currentUserId,
  } = useResolvedChatData(block)

  const {
    optimistic,
    addMessage,
    markResolvedByServer,
  } = useOptimisticMessages()

  const messagesRef = useRef<HTMLDivElement | null>(null)

  // =========================
  // 🧠 sync optimistic
  // =========================

  useEffect(() => {
    markResolvedByServer(messages)
  }, [messages, markResolvedByServer])

  const allMessages = useMemo(
    () => mergeMessages(messages, optimistic),
    [messages, optimistic]
  )

  // =========================
  // 📜 AUTO SCROLL (ЕДИНСТВЕННЫЙ)
  // =========================

  useAutoScroll(
    block.features?.autoScroll,
    messagesRef,
    allMessages.length
  )

  // =========================
  // ⚡ realtime
  // =========================

  useRealtime(
    block.features?.realtime,
    thread?.id
  )

  // =========================
  // 🧩 состояния
  // =========================

  const isLoading = !thread || !thread.id
  const hasMessages = allMessages.length > 0

  // =========================
  // ❗ пустой чат (sidebar UX)
  // =========================

  if (!thread?.id) {
    return (
      <div className="chat-thread chat-thread--empty-state">
        <div className="chat-thread__empty">
          Выберите чат слева
        </div>
      </div>
    )
  }

  // =========================
  // 🎨 render
  // =========================

  return (
    <div className="chat-thread">

      {/* HEADER */}
      {block.features?.header && (
        <ChatHeader
          thread={thread}
          participants={
            block.features?.participants
              ? participants
              : []
          }
        />
      )}

      {/* MESSAGES */}
      <div
        ref={messagesRef}
        className="chat-thread__messages"
      >
        {isLoading && <ChatThreadSkeleton />}

        {!isLoading && !hasMessages && (
          <ChatThreadEmpty />
        )}

        {!isLoading && hasMessages && (
          <ChatMessages
            messages={allMessages}
            currentUserId={currentUserId}
            grouping={block.features?.grouping}
            timestamps={block.features?.timestamps}
          />
        )}
      </div>

      {/* COMPOSER */}
      {block.reply && !isLoading && (
        <ChatComposer
          action={
            typeof block.reply.submit === "string"
              ? block.reply.submit
              : block.reply.submit.action
          }
          ctx={block.reply.ctx}
          currentUserId={currentUserId}
          addOptimistic={addMessage}
        />
      )}

    </div>
  )
}