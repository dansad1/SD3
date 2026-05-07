import { useContext } from "react"
import { PageContext } from "./context"

export function usePageApi() {
  const ctx = useContext(PageContext)

  if (!ctx) {
    throw new Error(
      "usePageApi must be used inside <PageContext.Provider>"
    )
  }

  return ctx
}