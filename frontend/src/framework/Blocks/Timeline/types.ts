import type { BaseBlock } from "../BlockType"

export type TimelineBlock = BaseBlock & {
  type: "timeline"

  items?: unknown[]
  source?: string
  params?: Record<string, unknown>

  compact?: boolean
  reverse?: boolean
  groupByDate?: boolean
  emptyText?: string
}