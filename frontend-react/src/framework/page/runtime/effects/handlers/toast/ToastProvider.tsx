import {
  useCallback,
  useMemo,
  useState,
  type ReactNode,
} from "react"
import { ToastContext, type ToastItem, type ToastVariant } from "./ToastContext"



export function ToastProvider({
  children,
}: {
  children: ReactNode
}) {
  const [items, setItems] = useState<
    ToastItem[]
  >([])

  console.log(
    "[ToastProvider] render",
    items
  )

  const remove = useCallback((id: string) => {
    console.log(
      "[ToastProvider] remove",
      id
    )

    setItems(prev =>
      prev.filter(item => item.id !== id)
    )
  }, [])

  const show = useCallback(
    ({
      title,
      description,
      variant = "info",
    }: {
      title: string
      description?: string
      variant?: ToastVariant
    }) => {
      const id = crypto.randomUUID()

      const item: ToastItem = {
        id,
        title,
        description,
        variant,
      }

      console.log(
        "[ToastProvider] show",
        item
      )

      setItems(prev => {
        const next = [...prev, item]

        console.log(
          "[ToastProvider] next items",
          next
        )

        return next
      })

      window.setTimeout(() => {
        console.log(
          "[ToastProvider] auto remove",
          id
        )

        remove(id)
      }, 4000)
    },
    [remove]
  )

  const value = useMemo(
    () => ({
      items,
      show,
      remove,
    }),
    [items, show, remove]
  )

  console.log(
    "[ToastProvider] context value",
    value
  )

  return (
    <ToastContext.Provider value={value}>
      {children}
    </ToastContext.Provider>
  )
}