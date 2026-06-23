import type {
  TableCtrlBase,
  BaseRow,
} from "@/framework/Blocks/Table/types/runtime"
import { TableCell } from "./TableCell"


export function DefaultTableRow<
  T extends BaseRow,
>({
  row,
  ctrl,
}: {
  row: T
  ctrl: TableCtrlBase<T>
}) {
  const {
    fields,
    sort,
    selection,
    rowActions,
    onRowAction,
    onRowClick,
  } = ctrl

  const hasSelection =
    Boolean(selection)

  const hasRowActions =
    Boolean(rowActions?.length)

  const hasRowClick =
    Boolean(onRowClick)

  return (
    <tr
      className={
        hasRowClick
          ? "clickable-row"
          : undefined
      }
      onClick={(e) => {

        if (!hasRowClick) {
          return
        }

        const target =
          e.target as HTMLElement

        if (
          target.closest(
            "input,button,a,label,select,textarea,[role='checkbox']"
          )
        ) {
          return
        }

        onRowClick?.(row)
      }}
    >
      {hasSelection &&
        selection && (
          <td>
            <input
              type="checkbox"
              checked={selection.selected.has(
                row.id
              )}
              onChange={() => {
                selection.toggle(
                  row.id
                )
              }}
            />
          </td>
        )}

      {fields.map((field) => (
        <td
          key={field.key}
          className={
            sort?.key === field.key
              ? "active-sort"
              : undefined
          }
        >
          <TableCell
            field={field}
            row={row}
          />
        </td>
      ))}

      {hasRowActions &&
        rowActions && (
          <td>
            <div
              style={{
                display: "flex",
                gap: 6,
              }}
            >
              {rowActions.map(
                (action) => (
                  <button
                    key={action.key}
                    type="button"
                    className={
                      `ui-btn ui-btn-${action.variant ?? "secondary"}`
                    }
                    onClick={(e) => {
                      e.preventDefault()
                      e.stopPropagation()

                      onRowAction?.(
                        action.key,
                        row
                      )
                    }}
                  >
                    {action.label}
                  </button>
                )
              )}
            </div>
          </td>
        )}
    </tr>
  )
}