import Input from "../../ui/Input"
import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

export const NumberInputWidget: WidgetRenderer = (
  props
) => {
  const { value, onChange } = props

  return (
    <BaseWidget {...props}>
      {({ disabled }) => (
        <Input
          type="number"
          value={value == null ? "" : String(value)}
          onChange={v =>
            onChange(v === "" ? null : Number(v))
          }
          disabled={disabled}
        />
      )}
    </BaseWidget>
  )
}