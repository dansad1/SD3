import type {
  SemanticRendererProps
} from "@/framework/renderers/types"

type AttendanceValue = {
  attended?: boolean | null
  grade?: number | null
}

export const AttendanceCell = ({
  value,
  onChange,
}: SemanticRendererProps<AttendanceValue>) => {

  const attended =
    value?.attended ?? null

  const grade =
    value?.grade ?? null

  return (
    <div
      style={{
        display: "flex",
        gap: 4,
      }}
    >

      <button
        onClick={() =>
          onChange?.({
            ...value,
            attended:
              attended === true
                ? false
                : true,
          })
        }
      >
        {
          attended === true
            ? "✔"
            : attended === false
              ? "✖"
              : "—"
        }
      </button>

      <input
        type="number"
        value={grade ?? ""}
        onChange={e =>
          onChange?.({
            ...value,
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