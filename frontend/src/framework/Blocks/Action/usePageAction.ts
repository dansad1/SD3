import type { PageActionHandler } from "@/framework/page/context/types"
import { usePageApi } from "@/framework/page/context/usePageApi"
import { useEffect } from "react"

export function usePageAction(
  actionId: string,
  handler: PageActionHandler
) {
  const { registerHandler, unregisterHandler } = usePageApi()

  useEffect(() => {
    registerHandler(actionId, handler)

    return () => {
      unregisterHandler(actionId, handler.id)
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [
    actionId,
    handler.id,
    handler.label,
    handler.icon,
    handler.variant,
    handler.order,
      handler.placement, // 🔥 ВАЖНО

    registerHandler,
    unregisterHandler,
  ])
}