import type {
  TableCtrlBase,
  BaseRow,
} from "@/framework/Blocks/Table/types/runtime"

import { DefaultTableRow }
  from "./DefaultTableRow"
import { AccordionTableRow } from "./AccordionTableRow"


export function TableRow<
  T extends BaseRow
>({
  row,
  ctrl,
}: {
  row: T
  ctrl: TableCtrlBase<T>
}) {

  switch (
    ctrl.rowVariant
  ) {

    case "accordion":

      return (
        <AccordionTableRow
          row={row}
          ctrl={ctrl}
        />
      )

    default:

      return (
        <DefaultTableRow
          row={row}
          ctrl={ctrl}
        />
      )
  }
}