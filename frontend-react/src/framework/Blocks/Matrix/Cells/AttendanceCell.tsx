import type { MatrixCellValue } from "../types"

type Props = {
  value: MatrixCellValue
  onChange: (patch: Partial<MatrixCellValue>) => void
}

export const AttendanceCell = ({ value, onChange }: Props) => {
  const attended = value?.attended ?? null
  const grade = value?.grade ?? null

  return (
    <div style={{ display: "flex", gap: 4 }}>
      {/* attendance toggle */}
      <button
        onClick={() =>
          onChange({
            attended: attended === true ? false : true,
          })
        }
      >
        {attended === true ? "✔" : attended === false ? "✖" : "—"}
      </button>

      {/* grade */}
      <input
        type="number"
        value={grade ?? ""}
        onChange={e =>
          onChange({
            grade:
              e.target.value === ""
                ? null
                : Number(e.target.value),
          })
        }
        style={{ width: 50 }}
      />
    </div>
  )
}