// src/framework/Blocks/Chat/features/useChatListData.ts

import { useMemo } from "react"

import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import { resolveRuntimeValue } from "../ChatThread/runtime"
import type { ChatListItem } from "./types"


export function useChatListData(block: {
  data?: unknown
  selectedId?: unknown
}) {
  const runtime = usePageRuntimeContext()

  const items = useMemo(() => {
    const value = resolveRuntimeValue(block.data, runtime)

    return Array.isArray(value)
      ? (value as ChatListItem[])
      : []
  }, [block.data, runtime])

  const selectedId = useMemo(() => {
    const value = resolveRuntimeValue(
      block.selectedId,
      runtime
    )

    return value != null ? String(value) : ""
  }, [block.selectedId, runtime])

  return {
    items,
    selectedId,
  }
}