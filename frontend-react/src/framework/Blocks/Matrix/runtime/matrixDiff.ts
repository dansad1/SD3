import type { MatrixCellValue, MatrixChange } from "../types"

export function buildMatrixChanges(
  current: Record<string, MatrixCellValue>,
  initial: Record<string, MatrixCellValue>
): MatrixChange[] {
  const changes: MatrixChange[] = []

  for (const key in current) {
    const curr = current[key]
    const init = initial[key]

    if (JSON.stringify(curr) !== JSON.stringify(init)) {
      const [y, x] = key.split(":")

      changes.push({
        x,
        y,
        value: curr,
      })
    }
  }

  return changes
}