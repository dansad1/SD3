import { useContext } from "react"
import { ToastContext } from "./ToastContext"

export function useToast() {
  const ctx = useContext(ToastContext)

  console.log("[useToast] ctx", ctx)

  if (!ctx) {
    throw new Error(
      "useToast must be used inside ToastProvider"
    )
  }

  return ctx
}