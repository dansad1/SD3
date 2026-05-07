import { AttendanceCell } from "./Cells/AttendanceCell"
import { NumberCell } from "./Cells/NumberCell"
import { SelectCell } from "./Cells/SelectCell"
import { TextCell } from "./Cells/TextCell"
import type { MatrixCellSchema, MatrixCellValue } from "./types"


type Props = {
  schema?: MatrixCellSchema
  value: MatrixCellValue
  onChange: (patch: Partial<MatrixCellValue>) => void
}

function resolveWidget(
  schema: MatrixCellSchema | undefined,
  value: MatrixCellValue
): MatrixCellSchema["widget"] {
  if (schema?.widget) return schema.widget

  if ("attended" in value || "grade" in value) {
    return "attendance"
  }

  if (typeof value?.value === "number") {
    return "number"
  }

  if (typeof value?.value === "string") {
    return "text"
  }

  return "text"
}

export const MatrixCell = ({ schema, value, onChange }: Props) => {
  const widget = resolveWidget(schema, value)

  switch (widget) {
    case "select":
      return (
        <SelectCell
          schema={schema}
          value={value}
          onChange={onChange}
        />
      )

    case "number":
      return (
        <NumberCell value={value} onChange={onChange} />
      )

    case "attendance":
      return (
        <AttendanceCell value={value} onChange={onChange} />
      )

    case "text":
    default:
      return (
        <TextCell value={value} onChange={onChange} />
      )
  }
}