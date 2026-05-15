// src/framework/security/CapabilityContext.ts

import { createContext } from "react"
import type { BlockCapabilities } from "../Blocks/BlockType"


export const CapabilityContext =
  createContext<BlockCapabilities | undefined>(
    undefined
  )