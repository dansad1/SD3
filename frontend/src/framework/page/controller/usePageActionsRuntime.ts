// usePageActionsRuntime.ts

import { useCallback, useRef, useState } from "react"

import type { ActionContext } from "../../Blocks/Action/types"
import type { ActionDescriptor } from "@/framework/Blocks/Action/types"
import type {
  ActionRuntime,
  PageActionHandler,
  PageRunResult,
} from "../context/types"

import { buildActions } from "./actions/buildActions"
import { registerHandlerRuntime } from "./actions/registerHandler"
import { unregisterHandlerRuntime } from "./actions/unregisterHandler"
import { runPageAction } from "./actions/runPageAction"

export function usePageActionsRuntime() {
  const actionsRef = useRef<Record<string, ActionRuntime>>({})
  const [actions, setActions] = useState<ActionDescriptor[]>([])

  const recompute = useCallback(() => {
    const nextActions = buildActions(actionsRef.current)

    
    setActions(nextActions)
  }, [])

  const registerHandler = useCallback(
    (actionId: string, handler: PageActionHandler) => {
      

      const changed = registerHandlerRuntime(
        actionsRef.current,
        actionId,
        handler
      )

     

      if (changed) {
        recompute()
      }
    },
    [recompute]
  )

  const unregisterHandler = useCallback(
    (actionId: string, handlerId: string) => {
      

      const changed = unregisterHandlerRuntime(
        actionsRef.current,
        actionId,
        handlerId
      )

      

      if (changed) {
        recompute()
      }
    },
    [recompute]
  )

  const run = useCallback(
    async (
      actionId: string,
      ctx: ActionContext = {}
    ): Promise<PageRunResult> => {
      return runPageAction(
        actionsRef.current,
        actionId,
        ctx
      )
    },
    []
  )

  return {
    actions,
    registerHandler,
    unregisterHandler,
    run,
  }
}