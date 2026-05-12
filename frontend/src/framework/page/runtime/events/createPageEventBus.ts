import type {
  PageEventBus,
  PageEventHandler,
} from "./types"

type HandlerMap = Map<string, Set<PageEventHandler>>

export function createPageEventBus(): PageEventBus {
  const handlers: HandlerMap = new Map()

  function emit(event: string, payload?: unknown) {
    const bucket = handlers.get(event)

    if (!bucket || bucket.size === 0) {
      return
    }

    for (const handler of bucket) {
      try {
        handler(payload)
      } catch (error) {
        console.error(
          `[page-event-bus] handler failed for "${event}"`,
          error
        )
      }
    }
  }

  function on(event: string, handler: PageEventHandler) {
    let bucket = handlers.get(event)

    if (!bucket) {
      bucket = new Set()
      handlers.set(event, bucket)
    }

    bucket.add(handler)

    return () => {
      const current = handlers.get(event)

      if (!current) {
        return
      }

      current.delete(handler)

      if (current.size === 0) {
        handlers.delete(event)
      }
    }
  }

  return {
    emit,
    on,
  }
}