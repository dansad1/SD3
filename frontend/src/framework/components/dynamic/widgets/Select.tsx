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

  const options =
    field.options ?? []

  const normalizedValue =
    value &&
    typeof value === "object" &&
    "value" in value
      ? value.value
      : value

  return (
    <BaseWidget {...props}>

      {({ disabled }) => (

        <select
          className="ui-input ui-native-select"

          value={
            normalizedValue == null
              ? ""
              : String(normalizedValue)
          }

          onChange={e => {
            onChange(e.target.value)
          }}

          disabled={disabled}
        >

          <option value="">
            — выбрать —
          </option>

          {options.map(option => (

            <option
              key={String(option.value)}
              value={String(option.value)}
            >
              {option.label}
            </option>

          ))}

        </select>

      )}

    </BaseWidget>
  )
}