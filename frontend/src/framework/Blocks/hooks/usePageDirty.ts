// src/framework/Blocks/hooks/usePageDirty.ts

import { usePageApi } from "@/framework/page/context/usePageApi"
import { useEffect } from "react"

export function usePageDirty(sourceId: string, dirty: boolean) {
  const { setDirty, unregisterDirty } = usePageApi()

  /* ================= SET DIRTY ================= */

  useEffect(() => {
    setDirty(sourceId, dirty)
  }, [sourceId, dirty, setDirty])

  /* ================= CLEANUP ================= */

  useEffect(() => {
    return () => {
      unregisterDirty(sourceId)
    }
  }, [sourceId, unregisterDirty])
}