import type {
  PageActionHandler,
} from "@/framework/page/context/types"

import { usePageApi }
  from "@/framework/page/context/usePageApi"

import { useEffect } from "react"

export function usePageAction(
  actionId: string,
  handler: PageActionHandler
) {

  const {
    registerHandler,
    unregisterHandler,
  } = usePageApi()

  /* ========================================== */
  /* REGISTER + UPDATE */
  /* ========================================== */

  useEffect(() => {

    registerHandler(
      actionId,
      handler
    )

  }, [

    actionId,

    handler,

    registerHandler,

  ])

  /* ========================================== */
  /* UNREGISTER ONLY ON UNMOUNT */
  /* ========================================== */

  useEffect(() => {

    return () => {

      unregisterHandler(
        actionId,
        handler.id
      )
    }

  }, [

    actionId,

    handler.id,

    unregisterHandler,

  ])
}