import { createContext } from "react"

export type ToastVariant =
  | "success"
  | "error"
  | "info"
  | "warning"

export type ToastItem = {
  id: string
  title: string
  description?: string
  variant: ToastVariant
}

export type ToastContextValue = {
  items: ToastItem[]
  show: (toast: {
    title: string
    description?: string
    variant?: ToastVariant
  }) => void
  remove: (id: string) => void
}

export const ToastContext =
  createContext<ToastContextValue | null>(null)