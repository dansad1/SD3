import type { ReactNode } from "react"

export function PageRoot({
  mode,
  children,
}: {
  mode: "auth" | "app"
  children: ReactNode
}) {
  return (
    <div className={`page-root mode-${mode}`}>
      {children}
    </div>
  )
}
