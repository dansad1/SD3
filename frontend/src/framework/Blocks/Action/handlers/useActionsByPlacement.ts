// src/framework/Blocks/Action/hooks/useActionsByPlacement.ts

import { useMemo } from "react"

import { usePageActions } from "./usePageActions"

import type { ActionDescriptor } from "../types"


export function useActionsByPlacement(
  placement: string,
): ActionDescriptor[] {

  const actions =
    usePageActions()

  return useMemo(() => {

    return actions.filter(
      action =>
        action.placement === placement
    )

  }, [
    actions,
    placement,
  ])
}