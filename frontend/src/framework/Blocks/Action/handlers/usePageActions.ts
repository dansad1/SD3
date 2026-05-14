// src/framework/Blocks/Action/hooks/usePageActions.ts

import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"


export function usePageActions() {

  const runtime =
    usePageRuntimeContext()

  return runtime.actions
}