import type { MatrixCellSchema, MatrixCellValue } from "../types"

type Props = {
  schema?: MatrixCellSchema
  value: MatrixCellValue
  onChange: (patch: Partial<MatrixCellValue>) => void
}

export const SelectCell = ({ schema, value, onChange }: Props) => {
  const v = value?.value ?? ""

  return (
    <select
      value={v}
      onChange={e =>
        onChange({
          value: e.target.value === "" ? null : e.target.value,
        })
      }
    >
      <option value="">—</option>

      {schema?.choices?.map(opt => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  )
}