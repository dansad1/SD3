import type { MatrixCellValue } from "../types"

type Props = {
  value: MatrixCellValue
  onChange: (patch: Partial<MatrixCellValue>) => void
}

export const NumberCell = ({ value, onChange }: Props) => {
  return (
    <input
      type="number"
      value={value?.value ?? ""}
      onChange={e =>
        onChange({
          value:
            e.target.value === ""
              ? null
              : Number(e.target.value),
        })
      }
    />
  )
}