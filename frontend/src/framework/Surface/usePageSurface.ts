import { useEffect } from "react"

import type { PageChrome } from "@/framework/page/PageSchema"
import { surfaceStore } from "./surfaceStore"
import { resolveSurface } from "./resolveSurface"

export function usePageSurface(chrome?: PageChrome) {
  useEffect(() => {
    console.log("🟦 USE PAGE SURFACE chrome:", chrome)

    const surface = resolveSurface(chrome)

    console.log("🟦 RESOLVED SURFACE:", surface)

    surfaceStore.init(surface)

    console.log("🟦 SURFACE AFTER INIT:", surfaceStore.get())
  }, [chrome])
}