import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

export const TextareaWidget: WidgetRenderer = (
  props
) => {
  const { value, onChange } = props

  return (
    <BaseWidget {...props}>
      {({ disabled }) => (
        <textarea
          className="ui-input"
          rows={4}
          value={value == null ? "" : String(value)}
          onChange={e => onChange(e.target.value)}
          disabled={disabled}
        />
      )}
    </BaseWidget>
  )
}