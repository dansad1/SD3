import type {
  TimelineChange,
  TimelineItem,
  TimelineViewModel,
} from "./useTimelineController"


const HIDDEN_FIELDS = new Set([
  "id",
  "pk",
  "created",
  "updated",
  "created_at",
  "updated_at",
  "deleted_at",
])

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

function getActionIcon(action: string) {
  switch (action) {
    case "create":
      return "+"

    case "update":
      return "↻"

    case "delete":
      return "×"

    case "comment":
      return "💬"

    case "attachment":
      return "📎"

    case "email":
      return "✉"

    case "system":
      return "⚙"

    default:
      return "•"
  }
}

function getChangeBefore(change: TimelineChange) {
  return change.before ?? change.old_value
}

function getChangeAfter(change: TimelineChange) {
  return change.after ?? change.new_value
}

function getVisibleChanges(
  changes?: Record<string, TimelineChange>
) {
  return Object.entries(changes || {}).filter(
    ([field]) => !HIDDEN_FIELDS.has(field)
  )
}

function renderChanges(
  item: TimelineItem
) {
  if (item.action === "create") {
    return null
  }

  const entries = getVisibleChanges(item.changes)

  if (!entries.length) {
    return null
  }

  return (
    <div className="timeline-changes">
      {entries.map(([field, change]) => {
        const before = getChangeBefore(change)
        const after = getChangeAfter(change)

        return (
          <div
            key={field}
            className="timeline-change"
          >
            <div className="timeline-change-label">
              {change.label || field}
            </div>

            <div className="timeline-change-body">
              <div className="timeline-value timeline-value-old">
                <span className="timeline-value-caption">
                  Было
                </span>

                <span className="timeline-value-text">
                  {formatValue(before)}
                </span>
              </div>

              <div className="timeline-value-arrow">
                ↓
              </div>

              <div className="timeline-value timeline-value-new">
                <span className="timeline-value-caption">
                  Стало
                </span>

                <span className="timeline-value-text">
                  {formatValue(after)}
                </span>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}

function renderCreateSummary(
  item: TimelineItem
) {
  if (item.action !== "create") {
    return null
  }

  const entries = getVisibleChanges(item.changes)

  if (!entries.length) {
    return (
      <div className="timeline-description">
        Объект был создан.
      </div>
    )
  }

  return (
    <div className="timeline-create-summary">
      {entries.map(([field, change]) => {
        const value = getChangeAfter(change)

        return (
          <div
            key={field}
            className="timeline-create-row"
          >
            <span className="timeline-create-label">
              {change.label || field}
            </span>

            <span className="timeline-create-value">
              {formatValue(value)}
            </span>
          </div>
        )
      })}
    </div>
  )
}

function renderMeta(item: TimelineItem) {
  const text = item.meta?.text
  const description = item.meta?.description

  const value =
    typeof text === "string"
      ? text
      : typeof description === "string"
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
  const date = item.created || item.date

  return (
    <div
      className={[
        "timeline-item",
        compact ? "timeline-item-compact" : "",
        `timeline-action-${item.action}`,
      ].join(" ")}
    >
      <div className="timeline-rail">
        <div className="timeline-marker">
          {getActionIcon(item.action)}
        </div>
      </div>

      <article className="timeline-card">
        <header className="timeline-card-header">
          <div>
            <div className="timeline-title">
              {getActionTitle(item)}
            </div>

            <div className="timeline-meta">
              <span>
                {item.actor?.label || "Система"}
              </span>

              {date && (
                <>
                  <span className="timeline-dot">
                    •
                  </span>

                  <span>
                    {formatDate(date)}
                  </span>
                </>
              )}
            </div>
          </div>

          <div className="timeline-badge">
            {item.action}
          </div>
        </header>

        {item.object_repr && (
          <div className="timeline-object">
            {item.object_repr}
          </div>
        )}

        {renderMeta(item)}
        {renderCreateSummary(item)}
        {renderChanges(item)}
      </article>
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

  const rows = ordered.map((item, index) => {
    const day = formatDay(item.created || item.date)

    const prev =
      index > 0
        ? ordered[index - 1]
        : null

    const prevDay = prev
      ? formatDay(prev.created || prev.date)
      : null

    return {
      item,
      day,
      showDay:
        Boolean(groupByDate) &&
        Boolean(day) &&
        day !== prevDay,
    }
  })

  if (loading) {
    return (
      <div className="timeline-state">
        Загрузка истории...
      </div>
    )
  }

  if (error) {
    return (
      <div className="timeline-state timeline-state-error">
        <div>{error}</div>

        <button
          type="button"
          onClick={reload}
          className="timeline-retry"
        >
          Повторить
        </button>
      </div>
    )
  }

  if (!rows.length) {
    return (
      <div className="timeline-state">
        {emptyText}
      </div>
    )
  }

  return (
    <div className="timeline">
      {rows.map(({ item, day, showDay }) => (
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
      ))}
    </div>
  )
}