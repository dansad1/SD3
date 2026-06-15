import { TimelineView } from "./TimelineView"
import type { TimelineBlock as TimelineBlockType } from "./types"
import { useTimelineController } from "./useTimelineController"

export function TimelineBlock({
  block,
}: {
  block: TimelineBlockType
}) {
  const vm = useTimelineController(block)

  return <TimelineView {...vm} />
}