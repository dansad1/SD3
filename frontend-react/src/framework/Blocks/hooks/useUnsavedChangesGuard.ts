// src/pages/page/hooks/useUnsavedChangesGuard.ts

import { useEffect } from "react"

export function useUnsavedChangesGuard(enabled: boolean) {
  useEffect(() => {
    if (!enabled) return

    const onBeforeUnload = (e: BeforeUnloadEvent) => {
      e.preventDefault()
      // Chrome требует returnValue
      e.returnValue = ""
      return ""
    }

    window.addEventListener("beforeunload", onBeforeUnload)
    return () => window.removeEventListener("beforeunload", onBeforeUnload)
  }, [enabled])
}