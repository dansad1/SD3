import type {
  TimelineChange,
  TimelineItem,
  TimelineViewModel,
} from "./useTimelineController"

function formatDate(value?: string) {
  if (!value) return ""

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleString()
}

function formatDay(value?: string) {
  if (!value) return ""

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
    return value
  }

  return date.toLocaleDateString()
}

function formatValue(value: unknown) {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return "—"
  }

  if (typeof value === "object") {
    try {
      return JSON.stringify(value)
    } catch {
      return String(value)
    }
  }

  return String(value)
}

function getActionTitle(item: TimelineItem) {
  const metaTitle = item.meta?.title

  if (typeof metaTitle === "string") {
    return metaTitle
  }

  switch (item.action) {
    case "create":
      return "Создан объект"

    case "update":
      return "Изменён объект"

    case "delete":
      return "Удалён объект"

    case "comment":
      return "Комментарий"

    case "attachment":
      return "Вложение"

    case "email":
      return "Письмо"

    case "system":
      return "Системное событие"

    default:
      return item.action
  }
}

function getChangeBefore(
  change: TimelineChange
) {
  return (
    change.before ??
    change.old_value
  )
}

function getChangeAfter(
  change: TimelineChange
) {
  return (
    change.after ??
    change.new_value
  )
}

function renderChanges(
  changes?: Record<
    string,
    TimelineChange
  >
) {
  const entries = Object.entries(
    changes || {}
  )

  if (!entries.length) {
    return null
  }

  return (
    <div className="timeline-changes">

      {entries.map(
        ([field, change]) => (

          <div
            key={field}
            className="timeline-change"
          >

            <div className="timeline-change-label">
              {change.label || field}
            </div>

            <div className="timeline-change-values">

              <span>
                {formatValue(
                  getChangeBefore(change)
                )}
              </span>

              <span>→</span>

              <span>
                {formatValue(
                  getChangeAfter(change)
                )}
              </span>

            </div>

          </div>
        )
      )}

    </div>
  )
}

function renderMeta(
  item: TimelineItem
) {
  const text = item.meta?.text

  const description =
    item.meta?.description

  const value =
    typeof text === "string"
      ? text
      : typeof description ===
        "string"
      ? description
      : null

  if (!value) {
    return null
  }

  return (
    <div className="timeline-description">
      {value}
    </div>
  )
}

function TimelineEntry({
  item,
  compact,
}: {
  item: TimelineItem
  compact: boolean
}) {
  const date =
    item.created || item.date

  return (
    <div
      className={[
        "timeline-item",

        compact
          ? "timeline-item-compact"
          : "",

        `timeline-action-${item.action}`,
      ].join(" ")}
    >

      <div className="timeline-marker" />

      <div className="timeline-content">

        <div className="timeline-header">

          <div className="timeline-title">
            {getActionTitle(item)}
          </div>

          <div className="timeline-date">
            {formatDate(date)}
          </div>

        </div>

        <div className="timeline-actor">
          {item.actor?.label ||
            "Система"}
        </div>

        {renderMeta(item)}

        {renderChanges(
          item.changes
        )}

      </div>

    </div>
  )
}

export function TimelineView({
  items,
  loading,
  error,
  emptyText,
  compact,
  reverse,
  groupByDate,
  reload,
}: TimelineViewModel) {

  const ordered = reverse
    ? [...items].reverse()
    : items

  const rows = ordered.map(
    (item, index) => {

      const day = formatDay(
        item.created || item.date
      )

      const prev =
        index > 0
          ? ordered[index - 1]
          : null

      const prevDay = prev
        ? formatDay(
            prev.created ||
              prev.date
          )
        : null

      return {
        item,
        day,
        showDay:
          Boolean(groupByDate) &&
          Boolean(day) &&
          day !== prevDay,
      }
    }
  )

  if (loading) {
    return (
      <div className="timeline timeline-loading">
        Загрузка истории...
      </div>
    )
  }

  if (error) {
    return (
      <div className="timeline timeline-error">

        <div>{error}</div>

        <button
          type="button"
          onClick={reload}
        >
          Повторить
        </button>

      </div>
    )
  }

  if (!rows.length) {
    return (
      <div className="timeline timeline-empty">
        {emptyText}
      </div>
    )
  }

  return (
    <div className="timeline">

      {rows.map(
        ({
          item,
          day,
          showDay,
        }) => (
          <div key={item.id}>

            {showDay && (
              <div className="timeline-day">
                {day}
              </div>
            )}

            <TimelineEntry
              item={item}
              compact={compact}
            />

          </div>
        )
      )}

    </div>
  )
}