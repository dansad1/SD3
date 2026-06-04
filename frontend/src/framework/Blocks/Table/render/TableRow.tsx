import type {
  TableCtrlBase,
  BaseRow,
} from "@/framework/Blocks/Table/types/runtime"
import { DefaultTableRow } from "./DefaultTableRow"


export function TableRow<
  T extends BaseRow,
>({
  row,
  ctrl,
}: {
  row: T
  ctrl: TableCtrlBase<T>
}) {
  return (
    <DefaultTableRow
      row={row}
      ctrl={ctrl}
    />
  )
}