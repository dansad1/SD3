// src/framework/security/CapabilityBoundary.tsx

import {
  useContext,
  useMemo,
} from "react"

import { CapabilityContext }
  from "./CapabilityContext"
import type { BlockCapabilities } from "../Blocks/BlockType"


function mergeCapabilities(
  parent?: BlockCapabilities,
  local?: BlockCapabilities
): BlockCapabilities | undefined {

  if (!parent) {
    return local
  }

  if (!local) {
    return parent
  }

  const result = {
    ...parent,
  }

  for (const [key, value]
    of Object.entries(local)) {

    if (value === false) {
      result[key] = false
    }
  }

  return result
}

export function CapabilityBoundary({
  capabilities,
  children,
}: {
  capabilities?: BlockCapabilities
  children: React.ReactNode
}) {

  const parent =
    useContext(CapabilityContext)

  const merged = useMemo(
    () =>
      mergeCapabilities(
        parent,
        capabilities
      ),
    [parent, capabilities]
  )

  return (
    <CapabilityContext.Provider value={merged}>
      {children}
    </CapabilityContext.Provider>
  )
}