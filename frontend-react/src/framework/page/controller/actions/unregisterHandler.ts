import type { ActionRuntime } from "../../context/types"

export function unregisterHandlerRuntime(
  map: Record<string, ActionRuntime>,
  actionId: string,
  handlerId: string
): boolean {
  const bucket = map[actionId]
  if (!bucket) return false

  const nextHandlers = bucket.handlers.filter(
    h => h.id !== handlerId
  )

  if (nextHandlers.length === bucket.handlers.length) {
    return false
  }

  if (nextHandlers.length === 0) {
    delete map[actionId]
  } else {
    map[actionId] = {
      ...bucket,
      handlers: nextHandlers,
    }
  }

  return true
}