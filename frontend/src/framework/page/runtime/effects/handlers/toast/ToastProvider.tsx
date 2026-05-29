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

  
  
  const remove = useCallback((id: string) => {

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

     

      setItems(prev => {
        const next = [...prev, item]

        

        return next
      })

      window.setTimeout(() => {
        

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

  

  return (
    <ToastContext.Provider value={value}>
      {children}
    </ToastContext.Provider>
  )
}