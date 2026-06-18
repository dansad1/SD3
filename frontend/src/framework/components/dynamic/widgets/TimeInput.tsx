import Input from "../../ui/Input"
import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

export const TimeInputWidget: WidgetRenderer = (
  props
) => {

  const {
    value,
    onChange,
  } = props

  const normalized =
    value == null
      ? ""
      : String(value).slice(0, 5)

  return (

    <BaseWidget {...props}>

      {({ disabled }) => (

        <Input
          type="time"

          step={60}

          value={normalized}

          onChange={onChange}

          disabled={disabled}
        />

      )}

    </BaseWidget>

  )

}