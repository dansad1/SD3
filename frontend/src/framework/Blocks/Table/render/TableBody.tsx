import type {
  TableCtrlBase,
  BaseRow,
} from "@/framework/Blocks/Table/types/runtime"
import { TableRow } from "./TableRow"


function getRowKey<T extends BaseRow>(
  row: T,
  index: number
) {
  return row.id ?? index
}

export function TableBody<T extends BaseRow>({
  ctrl,
  emptyMessage,
  totalCols,
}: {
  ctrl: TableCtrlBase<T>
  emptyMessage: string
  totalCols: number
}) {
  const {
    rows,
    isLoading,
  } = ctrl

  return (
    <tbody>
      {!isLoading &&
        rows.length === 0 && (
          <tr>
            <td
              colSpan={totalCols}
              className="empty"
            >
              {emptyMessage}
            </td>
          </tr>
        )}

      {rows.map((row, index) => (
        <TableRow
          key={getRowKey(
            row,
            index
          )}
          row={row}
          ctrl={ctrl}
        />
      ))}
    </tbody>
  )
}