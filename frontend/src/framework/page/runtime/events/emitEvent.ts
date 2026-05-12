import type { PageEventBus, PageEventPayload } from "./types"

export function emitEvent(
  bus: PageEventBus,
  event: string,
  payload?: PageEventPayload
) {
  bus.emit(event, payload)
}