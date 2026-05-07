import Input from "../../ui/Input"
import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

export const DateInputWidget: WidgetRenderer = (
  props
) => {
  const { value, onChange } = props

  return (
    <BaseWidget {...props}>
      {({ disabled }) => (
        <Input
          type="date"
          value={value == null ? "" : String(value)}
          onChange={onChange}
          disabled={disabled}
        />
      )}
    </BaseWidget>
  )
}