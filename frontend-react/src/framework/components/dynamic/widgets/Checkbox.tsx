import Checkbox from "../../ui/Checkbox"
import type { WidgetRenderer } from "../types"
import { BaseWidget } from "./Base"

export const CheckboxWidget: WidgetRenderer = (
  props
) => {

  const { field, value, onChange, loading } = props

  return (
    <BaseWidget
      field={field}
      loading={loading}
    >
      {({ disabled }) => (

        <Checkbox
          checked={Boolean(value)}
          onChange={onChange}
          disabled={disabled}
        />

      )}
    </BaseWidget>
  )
}