import type {
  TimelineChange,
  TimelineItem,
  TimelineViewModel,
} from "./useTimelineController"


// =========================================================
// FIELD POLICY
// =========================================================

const HIDDEN_FIELDS =
  new Set([
    "id",
    "pk",
    "created",
    "updated",
    "created_at",
    "updated_at",
    "deleted_at",
  ])


// =========================================================
// FORMATTERS
// =========================================================

function formatDate(
  value?: string,
  dateOnly = false
): string {
  if (!value) {
    return ""
  }

  const date =
    new Date(value)

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
    return value
  }

  return dateOnly
    ? date.toLocaleDateString()
    : date.toLocaleString()
}

function formatValue(
  value: unknown
): string {
  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return "—"
  }

  if (
    typeof value === "boolean"
  ) {
    return value
      ? "Да"
      : "Нет"
  }

  if (
    typeof value === "object"
  ) {
    try {
      return JSON.stringify(
        value
      )
    } catch {
      return String(value)
    }
  }

  return String(value)
}


// =========================================================
// ACTION
// =========================================================

function getActionTitle(
  item: TimelineItem
): string {
  const title =
    item.meta?.title

  if (
    typeof title === "string"
  ) {
    return title
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

function getActionIcon(
  action: string
): string {
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


// =========================================================
// CHANGES
// =========================================================

type VisibleChange = [
  string,
  TimelineChange,
]

function getVisibleChanges(
  item: TimelineItem
): VisibleChange[] {
  return Object.entries(
    item.changes ?? {}
  ).filter(
    ([field]) =>
      !HIDDEN_FIELDS.has(
        field
      )
  )
}

function Changes({
  item,
}: {
  item: TimelineItem
}) {
  if (
    item.action === "create"
  ) {
    return null
  }

  const changes =
    getVisibleChanges(
      item
    )

  if (!changes.length) {
    return null
  }

  return (
    <div className="timeline-changes">
      {changes.map(
        ([field, change]) => (
          <div
            key={field}
            className="timeline-change"
          >
            <div className="timeline-change-label">
              {change.label || field}
            </div>

            <div className="timeline-change-body">
              <div
                className={[
                  "timeline-value",
                  "timeline-value-old",
                ].join(" ")}
              >
                <span className="timeline-value-caption">
                  Было
                </span>

                <span className="timeline-value-text">
                  {formatValue(
                    change.before
                  )}
                </span>
              </div>

              <div className="timeline-value-arrow">
                ↓
              </div>

              <div
                className={[
                  "timeline-value",
                  "timeline-value-new",
                ].join(" ")}
              >
                <span className="timeline-value-caption">
                  Стало
                </span>

                <span className="timeline-value-text">
                  {formatValue(
                    change.after
                  )}
                </span>
              </div>
            </div>
          </div>
        )
      )}
    </div>
  )
}


// =========================================================
// CREATE SUMMARY
// =========================================================

function CreateSummary({
  item,
}: {
  item: TimelineItem
}) {
  if (
    item.action !== "create"
  ) {
    return null
  }

  const changes =
    getVisibleChanges(
      item
    )

  if (!changes.length) {
    return (
      <div className="timeline-description">
        Объект был создан.
      </div>
    )
  }

  return (
    <div className="timeline-create-summary">
      {changes.map(
        ([field, change]) => (
          <div
            key={field}
            className="timeline-create-row"
          >
            <span className="timeline-create-label">
              {change.label || field}
            </span>

            <span className="timeline-create-value">
              {formatValue(
                change.after
              )}
            </span>
          </div>
        )
      )}
    </div>
  )
}


// =========================================================
// META
// =========================================================

function Description({
  item,
}: {
  item: TimelineItem
}) {
  const text =
    item.meta?.text

  const description =
    item.meta?.description

  const value =
    typeof text === "string"
      ? text
      : (
          typeof description ===
          "string"
            ? description
            : null
        )

  if (!value) {
    return null
  }

  return (
    <div className="timeline-description">
      {value}
    </div>
  )
}


// =========================================================
// ENTRY
// =========================================================

function TimelineEntry({
  item,
  compact,
}: {
  item: TimelineItem
  compact: boolean
}) {
  const className = [
    "timeline-item",

    compact
      ? "timeline-item-compact"
      : "",

    `timeline-action-${item.action}`,
  ]
    .filter(Boolean)
    .join(" ")

  return (
    <div className={className}>
      <div className="timeline-rail">
        <div className="timeline-marker">
          {getActionIcon(
            item.action
          )}
        </div>
      </div>

      <article className="timeline-card">
        <header className="timeline-card-header">
          <div>
            <div className="timeline-title">
              {getActionTitle(
                item
              )}
            </div>

            <div className="timeline-meta">
              <span>
                {item.actor?.label ||
                  "Система"}
              </span>

              {item.date && (
                <>
                  <span className="timeline-dot">
                    •
                  </span>

                  <span>
                    {formatDate(
                      item.date
                    )}
                  </span>
                </>
              )}
            </div>
          </div>

          <div className="timeline-badge">
            {item.action}
          </div>
        </header>

        {item.objectRepr && (
          <div className="timeline-object">
            {item.objectRepr}
          </div>
        )}

        <Description
          item={item}
        />

        <CreateSummary
          item={item}
        />

        <Changes
          item={item}
        />
      </article>
    </div>
  )
}


// =========================================================
// STATE
// =========================================================

function LoadingState() {
  return (
    <div className="timeline-state">
      Загрузка истории...
    </div>
  )
}

function ErrorState({
  error,
  reload,
}: {
  error: string
  reload: () => void
}) {
  return (
    <div
      className={[
        "timeline-state",
        "timeline-state-error",
      ].join(" ")}
    >
      <div>
        {error}
      </div>

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

function EmptyState({
  text,
}: {
  text: string
}) {
  return (
    <div className="timeline-state">
      {text}
    </div>
  )
}


// =========================================================
// VIEW
// =========================================================

export function AuditTimelineView({
  items,
  loading,
  error,
  emptyText,
  compact,
  reverse,
  groupByDate,
  reload,
}: TimelineViewModel) {
  if (loading) {
    return (
      <LoadingState />
    )
  }

  if (error) {
    return (
      <ErrorState
        error={error}
        reload={reload}
      />
    )
  }

  const ordered =
    reverse
      ? [...items].reverse()
      : items

  if (!ordered.length) {
    return (
      <EmptyState
        text={emptyText}
      />
    )
  }

  return (
    <div className="timeline">
      {ordered.map(
        (
          item,
          index
        ) => {
          const day =
            formatDate(
              item.date,
              true
            )

          const previous =
            index > 0
              ? ordered[index - 1]
              : null

          const previousDay =
            previous
              ? formatDate(
                  previous.date,
                  true
                )
              : ""

          const showDay =
            groupByDate &&
            Boolean(day) &&
            day !== previousDay

          return (
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
        }
      )}
    </div>
  )
}