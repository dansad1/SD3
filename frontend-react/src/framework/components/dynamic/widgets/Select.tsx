import { BaseWidget } from "./Base"
import type { WidgetRenderer } from "./types"

export const SelectWidget: WidgetRenderer = (
  props
) => {
  const { field, value, onChange } = props

  return (
    <BaseWidget {...props}>
      {({ disabled }) => (
        <select
          className="ui-input"
          value={value == null ? "" : String(value)}
          onChange={e => onChange(e.target.value)}
          disabled={disabled}
        >
          <option value="">— выбрать —</option>
          {field.choices?.map(c => (
            <option key={String(c.value)} value={c.value}>
              {c.label}
            </option>
          ))}
        </select>
      )}
    </BaseWidget>
  )
}