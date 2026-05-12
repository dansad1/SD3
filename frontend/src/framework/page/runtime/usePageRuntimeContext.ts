import { useContext } from "react"
import { PageRuntimeContext } from "./PageRuntimeContext"

/* ================= BASE ================= */

export function usePageRuntimeContext() {
  const ctx = useContext(PageRuntimeContext)

  if (!ctx) {
    throw new Error("usePageRuntimeContext must be used inside provider")
  }

  return ctx
}

/* ================= SELECTORS ================= */

export function useRuntimeUser() {
  return usePageRuntimeContext().user
}

export function useRuntimeData<T = Record<string, unknown>>() {
  return usePageRuntimeContext().data as T
}

export function useRuntimeParams() {
  return usePageRuntimeContext().params
}

export function useRuntimeQuery() {
  return usePageRuntimeContext().query
}