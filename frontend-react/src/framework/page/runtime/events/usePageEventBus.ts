import { useMemo } from "react"
import { createPageEventBus } from "./createPageEventBus"

export function usePageEventBus() {
  return useMemo(() => {
    return createPageEventBus()
  }, [])
}