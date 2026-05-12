import Input from "../../ui/Input"
import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

export const PasswordInputWidget: WidgetRenderer = (
  props
) => {
  const { value, onChange } = props

  return (
    <BaseWidget {...props}>
      {({ disabled }) => (
        <Input
          type="password"
          autoComplete="new-password"
          value={(value ?? "") as string}
          onChange={v => onChange(v)}
          disabled={disabled}
        />
      )}
    </BaseWidget>
  )
}