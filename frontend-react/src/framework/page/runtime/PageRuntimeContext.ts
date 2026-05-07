import { createContext } from "react"
import type { PageRuntimeContext as PageRuntimeContextType } from "@/framework/bind/types"

export const PageRuntimeContext =
  createContext<PageRuntimeContextType | null>(null)

PageRuntimeContext.displayName = "PageRuntimeContext"

export const PageRuntimeContextProvider =
  PageRuntimeContext.Provider