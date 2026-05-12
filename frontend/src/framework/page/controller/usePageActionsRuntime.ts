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

    console.log("🧮 RECOMPUTE ACTIONS", {
      runtime: actionsRef.current,
      nextActions,
    })

    setActions(nextActions)
  }, [])

  const registerHandler = useCallback(
    (actionId: string, handler: PageActionHandler) => {
      console.log("➕ REGISTER HANDLER REQUEST", {
        actionId,
        handlerId: handler.id,
        handler,
        before: actionsRef.current,
      })

      const changed = registerHandlerRuntime(
        actionsRef.current,
        actionId,
        handler
      )

      console.log("✅ REGISTER HANDLER RESULT", {
        actionId,
        handlerId: handler.id,
        changed,
        after: actionsRef.current,
      })

      if (changed) {
        recompute()
      }
    },
    [recompute]
  )

  const unregisterHandler = useCallback(
    (actionId: string, handlerId: string) => {
      console.log("➖ UNREGISTER HANDLER REQUEST", {
        actionId,
        handlerId,
        before: actionsRef.current,
      })

      const changed = unregisterHandlerRuntime(
        actionsRef.current,
        actionId,
        handlerId
      )

      console.log("🗑 UNREGISTER HANDLER RESULT", {
        actionId,
        handlerId,
        changed,
        after: actionsRef.current,
      })

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