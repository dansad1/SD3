import type { WidgetProps } from "../types"
import { BaseWidget } from "./Base"

export function TextInputWidget({ field, value, onChange, loading }: WidgetProps) {
  const disabled = Boolean(field.readonly) || Boolean(loading)

  return (
    <BaseWidget field={field} loading={loading}>
      <input
        className="ui-input"
        type="text"
        value={(value ?? "") as string}
        disabled={disabled}
        onChange={(e) => onChange(e.target.value)}
      />
    </BaseWidget>
  )
}