// src/framework/Blocks/Chat/useChatThread.ts

import { useMemo } from "react"

import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"

import {
  resolveRuntimeValue,
} from "./runtime"

import type {
  ChatParticipant,
  ChatMessage,
  ChatThreadData,
} from "./types"

export function useChatThread(block: {
  participants?: unknown
  messages?: unknown
  thread?: unknown
  currentUserId?: unknown
}) {
  const runtime = usePageRuntimeContext()

  const participants = useMemo(() => {
    const value = resolveRuntimeValue(
      block.participants,
      runtime
    )

    return Array.isArray(value)
      ? (value as ChatParticipant[])
      : []
  }, [block.participants, runtime])

  const messages = useMemo(() => {
    const value = resolveRuntimeValue(
      block.messages,
      runtime
    )

    return Array.isArray(value)
      ? (value as ChatMessage[])
      : []
  }, [block.messages, runtime])

  const thread = useMemo(() => {
    const value = resolveRuntimeValue(
      block.thread,
      runtime
    )

    return value &&
      typeof value === "object"
      ? (value as ChatThreadData)
      : null
  }, [block.thread, runtime])

  const currentUserId = useMemo(() => {
    const value = resolveRuntimeValue(
      block.currentUserId,
      runtime
    )

    return value != null
      ? String(value)
      : ""
  }, [block.currentUserId, runtime])

  return {
    participants,
    messages,
    thread,
    currentUserId,
  }
}