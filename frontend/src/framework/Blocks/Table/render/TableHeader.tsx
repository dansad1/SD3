import type {
  TableCtrlBase,
  BaseRow,
} from "@/framework/Blocks/Table/types/runtime"

function getSortDirection(
  sort:
    | {
        key: string
        direction: "asc" | "desc"
      }
    | undefined,
  key: string
) {
  if (!sort) return undefined
  if (sort.key !== key) return undefined
  return sort.direction
}

export function TableHeader<T extends BaseRow>({
  ctrl,
  enableSorting,
}: {
  ctrl: TableCtrlBase<T>
  enableSorting: boolean
}) {
  const {
    fields,
    sort,
    selection,
    rowActions,
  } = ctrl

  const hasSelection = Boolean(selection)
  const hasRowActions = Boolean(rowActions?.length)

  return (
    <thead>
      <tr>
        {hasSelection && selection && (
          <th style={{ width: 44 }}>
            <input
              type="checkbox"
              checked={selection.isAllSelected}
              onChange={() =>
                selection.toggleAll()
              }
            />
          </th>
        )}

        {fields.map((col) => {
          const sortable =
            enableSorting &&
            Boolean(sort) &&
            Boolean(col.sortable)

          const direction =
            getSortDirection(
              sort,
              col.key
            )

          return (
            <th
              key={col.key}
              className={[
                sortable
                  ? "sortable"
                  : "",
                direction
                  ? "active-sort"
                  : "",
              ]
                .filter(Boolean)
                .join(" ")}
              onClick={() =>
                sortable &&
                sort &&
                sort.set(col.key)
              }
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

        {hasRowActions && (
          <th style={{ width: 160 }}>
            Действия
          </th>
        )}
      </tr>
    </thead>
  )
}