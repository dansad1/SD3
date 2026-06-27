import { useEffect } from "react"

import type { PageChrome } from "@/framework/page/PageSchema"
import { surfaceStore } from "./surfaceStore"
import { resolveSurface } from "./resolveSurface"

export function usePageSurface(chrome?: PageChrome) {
  useEffect(() => {
    
    const surface = resolveSurface(chrome)


    surfaceStore.init(surface)

    
  }, [chrome])
}