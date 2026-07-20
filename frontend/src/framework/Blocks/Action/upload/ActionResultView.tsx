// src/framework/Blocks/Action/upload/ActionResultView.tsx

import {
  useMemo,
  useState,
} from "react"



type UnknownRecord = Record<
  string,
  unknown
>


type TableRow = {
  key: string
  values: UnknownRecord
  errors: UnknownRecord | null
}


function isRecord(
  value: unknown,
): value is UnknownRecord {
  return (
    typeof value === "object"
    && value !== null
    && !Array.isArray(value)
  )
}


function isPrimitive(
  value: unknown,
): boolean {
  return (
    value === null
    || value === undefined
    || typeof value === "string"
    || typeof value === "number"
    || typeof value === "boolean"
  )
}


function formatKey(
  value: string,
): string {
  return value
    .replace(
      /_/g,
      " ",
    )
    .replace(
      /\b\w/g,
      letter =>
        letter.toUpperCase(),
    )
}


function formatValue(
  value: unknown,
): string {
  if (
    value === null
    || value === undefined
    || value === ""
  ) {
    return "—"
  }

  if (value === true) {
    return "Да"
  }

  if (value === false) {
    return "Нет"
  }

  if (Array.isArray(value)) {
    return value
      .map(formatValue)
      .join(", ")
  }

  if (isRecord(value)) {
    return Object.entries(value)
      .map(
        ([key, nestedValue]) =>
          `${formatKey(key)}: ${formatValue(nestedValue)}`,
      )
      .join("; ")
  }

  return String(
    value,
  )
}


function flattenRecord(
  record: UnknownRecord,
): UnknownRecord {
  const result: UnknownRecord = {}

  for (const [
    key,
    value,
  ] of Object.entries(record)) {
    if (
      key === "data"
      && isRecord(value)
    ) {
      for (const [
        nestedKey,
        nestedValue,
      ] of Object.entries(value)) {
        result[nestedKey] =
          nestedValue
      }

      continue
    }

    if (
      isRecord(value)
      && Object.values(value)
        .every(isPrimitive)
    ) {
      for (const [
        nestedKey,
        nestedValue,
      ] of Object.entries(value)) {
        result[
          `${key}.${nestedKey}`
        ] = nestedValue
      }

      continue
    }

    result[key] = value
  }

  return result
}


function collectColumns(
  rows: TableRow[],
): string[] {
  const columns = new Set<string>()

  for (const row of rows) {
    for (const key of Object.keys(
      row.values,
    )) {
      columns.add(
        key,
      )
    }
  }

  return Array.from(
    columns,
  )
}


function normalizeErrors(
  value: unknown,
): UnknownRecord {
  if (!isRecord(value)) {
    return {}
  }

  return value
}


function buildRows(
  result: UnknownRecord,
): TableRow[] {
  const arrayEntry =
    Object.entries(result)
      .find(
        ([, value]) =>
          Array.isArray(value)
          && value.every(isRecord),
      )

  if (!arrayEntry) {
    return []
  }

  const [, rawRows] =
    arrayEntry

  const errors = normalizeErrors(
    result.errors,
  )

  return (
    rawRows as UnknownRecord[]
  ).map(
    (
      rawRow,
      index,
    ) => {
      const rowKey = String(
        rawRow.row
        ?? rawRow.id
        ?? index + 1,
      )

      return {
        key: rowKey,
        values: flattenRecord(
          rawRow,
        ),
        errors: isRecord(
          errors[rowKey],
        )
          ? errors[rowKey] as UnknownRecord
          : null,
      }
    },
  )
}


function getMeta(
  result: UnknownRecord,
): UnknownRecord {
  if (
    isRecord(result.meta)
  ) {
    return result.meta
  }

  return {}
}


function getErrorMessages(
  errors: UnknownRecord,
): string[] {
  const messages: string[] = []

  for (const [
    field,
    value,
  ] of Object.entries(errors)) {
    if (Array.isArray(value)) {
      for (const message of value) {
        messages.push(
          `${formatKey(field)}: ${formatValue(message)}`,
        )
      }

      continue
    }

    messages.push(
      `${formatKey(field)}: ${formatValue(value)}`,
    )
  }

  return messages
}


function StatusBadge({
  hasErrors,
}: {
  hasErrors: boolean
}) {
  return (
    <span
      className={[
        "action-result__badge",
        hasErrors
          ? "action-result__badge--error"
          : "action-result__badge--success",
      ].join(" ")}
    >
      {hasErrors
        ? "Есть ошибки"
        : "Готово"}
    </span>
  )
}


function MetaCards({
  meta,
}: {
  meta: UnknownRecord
}) {
  const entries =
    Object.entries(meta)
      .filter(
        ([, value]) =>
          isPrimitive(value),
      )

  if (entries.length === 0) {
    return null
  }

  return (
    <div className="action-result__summary">
      {entries.map(
        ([key, value]) => (
          <div
            className="action-result__summary-card"
            key={key}
          >
            <div className="action-result__summary-label">
              {formatKey(
                key,
              )}
            </div>

            <div className="action-result__summary-value">
              {formatValue(
                value,
              )}
            </div>
          </div>
        ),
      )}
    </div>
  )
}


function EmptyResult() {
  return (
    <div className="action-result__empty">
      Результат не содержит строк для отображения
    </div>
  )
}


function ResultTable({
  rows,
}: {
  rows: TableRow[]
}) {
  const [
    onlyErrors,
    setOnlyErrors,
  ] = useState(false)

  const columns = useMemo(
    () =>
      collectColumns(
        rows,
      ),
    [rows],
  )

  const visibleRows = useMemo(
    () =>
      onlyErrors
        ? rows.filter(
            row =>
              row.errors !== null,
          )
        : rows,
    [
      onlyErrors,
      rows,
    ],
  )

  const errorCount = rows.filter(
    row =>
      row.errors !== null,
  ).length

  return (
    <>
      <div className="action-result__toolbar">
        <div className="action-result__toolbar-info">
          <strong>
            {rows.length}
          </strong>

          <span>
            строк
          </span>

          {errorCount > 0 && (
            <>
              <span className="action-result__dot">
                •
              </span>

              <strong className="action-result__error-count">
                {errorCount}
              </strong>

              <span>
                с ошибками
              </span>
            </>
          )}
        </div>

        {errorCount > 0 && (
          <label className="action-result__filter">
            <input
              type="checkbox"
              checked={
                onlyErrors
              }
              onChange={
                event =>
                  setOnlyErrors(
                    event.target.checked,
                  )
              }
            />

            <span>
              Только ошибки
            </span>
          </label>
        )}
      </div>

      <div className="action-result__table-shell">
        <div className="action-result__table-scroll">
          <table className="action-result__table">
            <thead>
              <tr>
                {columns.map(
                  column => (
                    <th
                      key={column}
                    >
                      {formatKey(
                        column,
                      )}
                    </th>
                  ),
                )}

                <th className="action-result__status-column">
                  Статус
                </th>
              </tr>
            </thead>

            <tbody>
              {visibleRows.map(
                row => {
                  const hasErrors =
                    row.errors !== null

                  const messages =
                    row.errors
                      ? getErrorMessages(
                          row.errors,
                        )
                      : []

                  return (
                    <tr
                      className={
                        hasErrors
                          ? "action-result__row--error"
                          : undefined
                      }
                      key={row.key}
                    >
                      {columns.map(
                        column => (
                          <td
                            key={column}
                            title={
                              formatValue(
                                row.values[
                                  column
                                ],
                              )
                            }
                          >
                            <div className="action-result__cell">
                              {formatValue(
                                row.values[
                                  column
                                ],
                              )}
                            </div>
                          </td>
                        ),
                      )}

                      <td className="action-result__status-cell">
                        <StatusBadge
                          hasErrors={
                            hasErrors
                          }
                        />

                        {messages.length > 0 && (
                          <div className="action-result__errors">
                            {messages.map(
                              (
                                message,
                                index,
                              ) => (
                                <div
                                  className="action-result__error-message"
                                  key={`${row.key}-${index}`}
                                >
                                  {message}
                                </div>
                              ),
                            )}
                          </div>
                        )}
                      </td>
                    </tr>
                  )
                },
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}


export function ActionResultView({
  result,
}: {
  result: unknown
}) {
  if (!isRecord(result)) {
    return null
  }

  const rows = buildRows(
    result,
  )

  const meta = getMeta(
    result,
  )

  return (
    <section className="action-result">
      <div className="action-result__header">
        <div>
          <h3 className="action-result__heading">
            Предварительный просмотр
          </h3>

          <p className="action-result__description">
            Проверьте данные перед продолжением
          </p>
        </div>

        <StatusBadge
          hasErrors={
            rows.some(
              row =>
                row.errors !== null,
            )
          }
        />
      </div>

      <MetaCards
        meta={meta}
      />

      {rows.length > 0
        ? (
            <ResultTable
              rows={rows}
            />
          )
        : (
            <EmptyResult />
          )}
    </section>
  )
}