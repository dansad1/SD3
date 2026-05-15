// src/framework/security/useCan.ts

import { useMemo } from "react"

import { useCapabilities }
  from "./useCapabilities"

export function useCan(
  action: string,
  fallback = false
) {

  const capabilities =
    useCapabilities()

  return useMemo(() => {

    if (!capabilities) {
      return fallback
    }

    return capabilities[action] === true

  }, [capabilities, action, fallback])
}