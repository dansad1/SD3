import { createContext } from "react"
import type { PageApi } from "./types"

export const PageContext =
  createContext<PageApi>(null as unknown as PageApi)