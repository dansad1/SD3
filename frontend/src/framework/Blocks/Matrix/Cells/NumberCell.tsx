import type {
  ChangeEvent,
} from "react"

import type {
  MatrixCellValue,
} from "../types"


type Props = {
  value: MatrixCellValue
  onChange: (
    patch: Partial<MatrixCellValue>,
  ) => void
}


export const NumberCell = ({
  value,
  onChange,
}: Props) => {
  const handleChange = (
    event: ChangeEvent<HTMLInputElement>,
  ) => {
    const rawValue =
      event.currentTarget.value

    if (rawValue === "") {
      onChange({
        value: null,
      })

      return
    }

    const numberValue =
      Number(rawValue)

    if (!Number.isFinite(numberValue)) {
      return
    }

    onChange({
      value: numberValue,
    })
  }

  return (
    <input
      className="ui-matrix-number"
      type="number"
      inputMode="decimal"
      value={value?.value ?? ""}
      onChange={handleChange}
    />
  )
}