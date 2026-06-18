import Input from "../../ui/Input"
import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

export const DateTimeInputWidget: WidgetRenderer = (
  props
) => {

  const {
    value,
    onChange,
  } = props

  const normalized =
    value == null
      ? ""
      : String(value)
          .replace("Z", "")
          .slice(0, 16)

  return (

    <BaseWidget {...props}>

      {({ disabled }) => (

        <Input

          type="datetime-local"

          step={60}

          value={normalized}

          onChange={onChange}

          disabled={disabled}

        />

      )}

    </BaseWidget>

  )

}