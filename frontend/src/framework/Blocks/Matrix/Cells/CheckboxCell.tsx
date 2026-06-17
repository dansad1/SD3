import type {
  MatrixCellValue,
} from "../types"

type Props = {
  value: MatrixCellValue
  onChange: (
    patch: Partial<MatrixCellValue>
  ) => void
}
export function CheckboxCell({
  value,
  onChange,
}: Props) {
  return (

    <input
      type="checkbox"

      checked={
        !!value.value
      }
      onChange={e =>
        onChange({
          value:
            e.target.checked,
        })
      }
    />
  )
}