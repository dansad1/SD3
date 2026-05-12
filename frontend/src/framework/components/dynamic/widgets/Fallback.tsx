import Input from "../../ui/Input"
import { BaseWidget } from "./Base"
import type { WidgetProps } from "../types"

export default function FallbackWidget(
  props: WidgetProps
) {
  const { value, onChange } = props

  return (
    <BaseWidget {...props}>
      {({ disabled }) => (
        <Input
          value={value == null ? "" : String(value)}
          onChange={onChange}
          disabled={disabled}
        />
      )}
    </BaseWidget>
  )
}