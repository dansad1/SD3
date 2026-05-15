// src/framework/security/useCapabilities.ts

import { useContext } from "react"

import { CapabilityContext }
  from "./CapabilityContext"

export function useCapabilities() {
  return useContext(CapabilityContext)
}