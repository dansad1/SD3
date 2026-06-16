import type { WidgetProps } from "../types"

export function MetaWidget({
  value,
  field,
}: WidgetProps) {

  return (
    <div className="meta-widget">

      <div className="meta-widget-label">
        {field.label}
      </div>

      <div className="meta-widget-value">
        {String(value ?? "—")}
      </div>

    </div>
  )
}