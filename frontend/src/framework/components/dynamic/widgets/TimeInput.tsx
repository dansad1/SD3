import Input from "../../ui/Input"
import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

export const TimeInputWidget: WidgetRenderer = (props) => {
  const { value, onChange } = props

  return (
    <BaseWidget {...props}>
      {({ disabled }) => (
        <Input
          type="time"
          value={value == null ? "" : String(value)}
          onChange={onChange}
          disabled={disabled}
        />
      )}
    </BaseWidget>
  )
}