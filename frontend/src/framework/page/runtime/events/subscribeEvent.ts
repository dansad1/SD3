import type { PageEventBus, PageEventHandler } from "./types"

export function subscribeEvent(
  bus: PageEventBus,
  event: string,
  handler: PageEventHandler
) {
  return bus.on(event, handler)
}