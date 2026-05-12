import type { ActionDescriptor } from "@/framework/Blocks/Action/types"
import { sortHandlers } from "./sortHandlers"
import type { ActionRuntime } from "../../context/types"

export function buildActions(
  map: Record<string, ActionRuntime>
): ActionDescriptor[] {

  const next = Object.values(map)
    .map(action => {
      const handlers = sortHandlers(action.handlers)

      // ✅ берём только UI handler
      const uiHandler = handlers.find(h => h.label)

      if (!uiHandler) return null

      return {
        id: action.id,
        label: uiHandler.label ?? action.id,
        variant: uiHandler.variant,
        icon: uiHandler.icon,
        placement: uiHandler.placement, // 🔥 обязательно
      }
    })
    .filter(Boolean) as ActionDescriptor[]

  next.sort((a, b) =>
    a.label.localeCompare(b.label, "ru")
  )

  return next
}