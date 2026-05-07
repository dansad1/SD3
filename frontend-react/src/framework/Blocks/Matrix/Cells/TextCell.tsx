import type { MatrixCellValue } from "../types"

type Props = {
  value: MatrixCellValue
  onChange: (patch: Partial<MatrixCellValue>) => void
}

export const TextCell = ({ value, onChange }: Props) => {
  return (
    <input
      type="text"
      value={value?.value ?? ""}
      onChange={e =>
        onChange({
          value: e.target.value,
        })
      }
    />
  )
}