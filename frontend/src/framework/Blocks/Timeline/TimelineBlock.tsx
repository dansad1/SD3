import { AuditTimelineView } from "./AuditTimelineView"
import type { TimelineBlock as TimelineBlockType } from "./types"
import { useTimelineController } from "./useTimelineController"

export function TimelineBlock({
  block,
}: {
  block: TimelineBlockType
}) {
  const viewModel =
    useTimelineController(
      block
    )

  return (
    <AuditTimelineView
      {...viewModel}
    />
  )
}