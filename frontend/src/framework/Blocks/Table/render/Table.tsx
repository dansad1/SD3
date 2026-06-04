import type { BaseRow, TableCtrlBase } from "../types/runtime"
import { TableBody } from "./TableBody"
import { TableHeader } from "./TableHeader"

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
    isLoading,
    error,
    selection,
    rowActions,
  } = ctrl

  if (error) {
    return (
      <div className="ui-table-error">
        {error}
      </div>
    )
  }

  if (!fields?.length) {
    if (isLoading) {
      return (
        <div className="ui-table-loading">
          Загрузка…
        </div>
      )
    }

    return (
      <div className="ui-table-error">
        Таблица не может быть отображена: нет колонок
      </div>
    )
  }

  const totalCols =
    fields.length +
    (selection ? 1 : 0) +
    (rowActions?.length ? 1 : 0)

  return (
    <div className="ui-table-wrapper">
      <table className="ui-table">

        <TableHeader
          ctrl={ctrl}
          enableSorting={enableSorting}
        />

        <TableBody
          ctrl={ctrl}
          totalCols={totalCols}
          emptyMessage={emptyMessage}
        />

      </table>

      {isLoading && (
        <div className="ui-table-loading-overlay">
          Загрузка…
        </div>
      )}
    </div>
  )
}