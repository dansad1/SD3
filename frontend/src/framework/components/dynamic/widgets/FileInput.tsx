import { BaseWidget } from "./Base"
import type { WidgetRenderer } from "./types"

export const FileInputWidget: WidgetRenderer = (
  props
) => {
  const { onChange } = props

  return (
    <BaseWidget {...props}>
      {({ disabled }) => (
        <input
          type="file"
          className="ui-input"
          onChange={e =>
            onChange(e.target.files?.[0] ?? null)
          }
          disabled={disabled}
        />
      )}
    </BaseWidget>
  )
}