import React from "react"
import type { TableCtrlBase, BaseRow } from "@/framework/Blocks/Table/types/runtime"
import type { Json } from "@/framework/types/json"

/* ================= HELPERS ================= */

function renderCell(value: Json) {
  if (value === null || value === undefined) return ""

  // допускаем расширение (UI может подмешать ReactNode)
  if (React.isValidElement(value)) return value

  if (typeof value === "object") {
    try {
      return JSON.stringify(value)
    } catch {
      return "[Object]"
    }
  }

  return String(value)
}

function getRowKey<T extends BaseRow>(row: T, index: number) {
  return row.id ?? index
}

function getSortDirection(
  sort: { key: string; direction: "asc" | "desc" } | undefined,
  key: string
) {
  if (!sort) return undefined
  if (sort.key !== key) return undefined
  return sort.direction
}

/* ================= COMPONENT ================= */

export default function Table<T extends BaseRow>({
  ctrl,
  enableSorting = true,
  emptyMessage = "Нет данных",
}: {
  ctrl: TableCtrlBase<T>
  enableSorting?: boolean
  emptyMessage?: string
}) {
  const {
    fields,
    rows,
    sort,
    selection,
    isLoading,
    rowActions,
    onRowAction,
    onRowClick,
  } = ctrl

  const hasSelection = Boolean(selection)
  const hasRowActions = Boolean(rowActions?.length)
  const hasRowClick = Boolean(onRowClick)

  const totalCols =
    fields.length +
    (hasSelection ? 1 : 0) +
    (hasRowActions ? 1 : 0)

  /* ================= STATES ================= */

  if (!fields?.length) {
    if (isLoading) {
      return <div className="ui-table-loading">Загрузка…</div>
    }

    return (
      <div className="ui-table-error">
        Таблица не может быть отображена: нет колонок
      </div>
    )
  }

  /* ================= RENDER ================= */

  return (
    <div className="ui-table-wrapper">
      <table className="ui-table">
        <thead>
          <tr>
            {/* selection */}
            {hasSelection && selection && (
              <th style={{ width: 44 }}>
                <input
                  type="checkbox"
                  checked={selection.isAllSelected}
                  onChange={() => selection.toggleAll()}
                  aria-label="Выбрать все"
                />
              </th>
            )}

            {/* columns */}
            {fields.map((col) => {
              const sortable =
                enableSorting &&
                Boolean(sort) &&
                Boolean(col.sortable)

              const direction = getSortDirection(sort, col.key)

              return (
                <th
                  key={col.key}
                  className={[
                    sortable ? "sortable" : "",
                    direction ? "active-sort" : "",
                  ]
                    .filter(Boolean)
                    .join(" ")}
                  onClick={() => sortable && sort && sort.set(col.key)}
                >
                  <span className="th-content">
                    {col.label}

                    {sortable && (
                      <span className="sort-indicator">
                        {direction === "asc"
                          ? "▲"
                          : direction === "desc"
                          ? "▼"
                          : "↕"}
                      </span>
                    )}
                  </span>
                </th>
              )
            })}

            {/* row actions */}
            {hasRowActions && <th style={{ width: 160 }}>Действия</th>}
          </tr>
        </thead>

        <tbody>
          {/* empty */}
          {!isLoading && rows.length === 0 && (
            <tr>
              <td colSpan={totalCols} className="empty">
                {emptyMessage}
              </td>
            </tr>
          )}

          {/* rows */}
          {rows.map((row, index) => (
            <tr
              key={getRowKey(row, index)}
              className={hasRowClick ? "clickable-row" : undefined}
              onClick={() => hasRowClick && onRowClick?.(row)}
            >
              {/* selection */}
              {hasSelection && selection && (
                <td>
                  <input
                    type="checkbox"
                    checked={selection.selected.has(row.id)}
                    onChange={(e) => {
                      e.stopPropagation()
                      selection.toggle(row.id)
                    }}
                  />
                </td>
              )}

              {/* cells */}
              {fields.map((col) => (
                <td
                  key={col.key}
                  className={
                    sort?.key === col.key ? "active-sort" : undefined
                  }
                >
                  {renderCell(row[col.key])}
                </td>
              ))}

              {/* actions */}
              {hasRowActions && rowActions && (
                <td>
                  <div style={{ display: "flex", gap: 6 }}>
                    {rowActions.map((a) => (
                      <button
                        type="button"
                        key={a.key}
                        className={`ui-btn ui-btn-${a.variant ?? "secondary"}`}
                        onClick={(e) => {
                          e.preventDefault()
                          e.stopPropagation()
                          onRowAction?.(a.key, row)
                        }}
                      >
                        {a.label}
                      </button>
                    ))}
                  </div>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>

      {/* loading overlay */}
      {isLoading && (
        <div className="ui-table-loading-overlay">Загрузка…</div>
      )}
    </div>
  )
}