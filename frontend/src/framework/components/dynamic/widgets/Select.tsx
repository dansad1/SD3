import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

export const SelectWidget: WidgetRenderer = (
  props
) => {

  const {
    field,
    value,
    onChange,
  } = props

  return (
    <BaseWidget {...props}>

      {({ disabled }) => (

        <select
          className="ui-input ui-native-select"

          value={
            value == null
              ? ""
              : String(value)
          }

          onChange={e => {
            onChange(e.target.value)
          }}

          disabled={disabled}
        >

          <option value="">
            — выбрать —
          </option>

          {field.choices?.map(option => (

            <option
              key={String(option.value)}
              value={option.value}
            >
              {option.label}
            </option>

          ))}

        </select>

      )}

    </BaseWidget>
  )
}