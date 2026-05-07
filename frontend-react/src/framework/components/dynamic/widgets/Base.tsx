import type { ReactNode } from "react"
import type { WidgetProps } from "../types"

type RenderFn = (ctx: { disabled: boolean }) => ReactNode

type Props = Pick<WidgetProps, "field" | "loading"> & {
  children: ReactNode | RenderFn
}

export function BaseWidget({ field, loading, children }: Props) {

  const disabled = Boolean(field.readonly) || Boolean(loading)

  const content =
    typeof children === "function"
      ? (children as RenderFn)({ disabled })
      : children

  return (
    <div className={`ui-widget ${disabled ? "ui-widget-disabled" : ""}`}>

      {loading && (
        <div className="ui-widget-loading">
          Загрузка...
        </div>
      )}

      {content}

    </div>
  )
}