import { Fragment, useState } from "react"

import type {
  BaseRow,
  TableCtrlBase,
} from "@/framework/Blocks/Table/types/runtime"

import { TableCell } from "./TableCell"

type Props<T extends BaseRow> = {
  row: T
  ctrl: TableCtrlBase<T>
}

function renderDetailValue(
  value: unknown
): string {
  if (
    value === null ||
    value === undefined
  ) {
    return ""
  }

  if (
    Array.isArray(value)
  ) {
    return value
      .map(renderDetailValue)
      .join(", ")
  }

  if (
    typeof value === "object"
  ) {

    if (
      value &&
      "label" in value
    ) {
      return String(
        (
          value as {
            label: unknown
          }
        ).label
      )
    }

    try {
      return JSON.stringify(
        value,
        null,
        2
      )
    } catch {
      return "[Object]"
    }
  }

  return String(value)
}

export function AccordionTableRow<
  T extends BaseRow
>({
  row,
  ctrl,
}: Props<T>) {

  const [
    expanded,
    setExpanded,
  ] = useState(false)

  const {
    fields,
    selection,
    rowActions,
    onRowAction,
  } = ctrl

  const totalCols =
    fields.length +
    (selection ? 1 : 0) +
    (rowActions?.length ? 1 : 0)

  return (
    <Fragment>

      <tr
        className="accordion-row"
        onClick={() =>
          setExpanded(
            value => !value
          )
        }
      >

        {selection && (

          <td>

            <input
              type="checkbox"
              checked={
                selection.selected.has(
                  row.id
                )
              }
              onChange={(e) => {

                e.stopPropagation()

                selection.toggle(
                  row.id
                )
              }}
            />

          </td>

        )}

        {fields.map(field => (

          <td
            key={field.key}
          >

            <TableCell
              field={field}
              row={row}
            />

          </td>

        ))}

        {rowActions?.length ? (

          <td>

            <div
              style={{
                display: "flex",
                gap: 6,
              }}
            >

              {rowActions.map(
                action => (

                  <button
                    key={action.key}
                    type="button"
                    className={`ui-btn ui-btn-${action.variant ?? "secondary"}`}
                    onClick={(e) => {

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

        ) : null}

      </tr>

      {expanded && (

        <tr
          className="accordion-details-row"
        >

          <td
            colSpan={totalCols}
          >

            <div
              className="accordion-details"
            >

              {Object.entries(
                row
              ).map(
                ([key, value]) => {

                  if (
                    key === "id"
                  ) {
                    return null
                  }

                  return (
                    <div
                      key={key}
                    >

                      <strong>
                        {key}
                      </strong>

                      {": "}

                      {renderDetailValue(
                        value
                      )}

                    </div>
                  )
                }
              )}

            </div>

          </td>

        </tr>

      )}

    </Fragment>
  )
}