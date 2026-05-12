import type { ActionRuntime, PageActionHandler } from "../../context/types"

export function registerHandlerRuntime(
  map: Record<string, ActionRuntime>,
  actionId: string,
  handler: PageActionHandler
): boolean {
  const bucket =
    map[actionId] ??
    (map[actionId] = {
      id: actionId,
      label: handler.label ?? actionId,
      handlers: [],
    })

  const index = bucket.handlers.findIndex(
    h => h.id === handler.id
  )

  // 🔥 КЛЮЧЕВОЙ ФИКС
  if (index >= 0) {
    return false // ❗ не обновляем вообще
  }

  map[actionId] = {
    ...bucket,
    handlers: [...bucket.handlers, handler],
  }

  return true
}