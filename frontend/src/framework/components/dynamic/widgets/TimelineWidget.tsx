import { useMemo } from "react"

import {
  useTimelineController,
} from "@/framework/Blocks/Timeline/useTimelineController"

import type {
  TimelineChange,
  TimelineItem,
  TimelineViewModel,
} from "@/framework/Blocks/Timeline/useTimelineController"

import type { WidgetProps } from "../types"
import { BaseWidget } from "./Base"


// =========================================================
// FIELD POLICY
// =========================================================

const HIDDEN_FIELDS = new Set([
  "id",
  "pk",
  "created",
  "updated",
  "created_at",
  "updated_at",
  "deleted_at",
])


// =========================================================
// HELPERS
// =========================================================

function getTicketId(
  value: WidgetProps["value"]
): string | number | null {
  if (
    typeof value === "string" ||
    typeof value === "number"
  ) {
    if (String(value).trim()) {
      return value
    }
  }

  if (typeof window === "undefined") {
    return null
  }

  const query = new URLSearchParams(
    window.location.search
  )

  return query.get("id")
}

function formatDate(
  value?: string,
  dateOnly = false
): string {
  if (!value) {
    return ""
  }

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) {
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

  if (typeof value === "boolean") {
    return value
      ? "Да"
      : "Нет"
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

function getActionTitle(
  item: TimelineItem
): string {
  const title = item.meta?.title

  if (typeof title === "string") {
    return title
  }

  switch (item.action) {
    case "create":
      return "Заявка создана"

    case "update":
      return "Заявка изменена"

    case "delete":
      return "Заявка удалена"

    case "status":
      return "Статус изменён"

    case "assign":
      return "Изменён исполнитель"

    case "sla":
      return "Изменён срок"

    case "priority":
      return "Изменён приоритет"

    case "type":
      return "Изменён тип заявки"

    case "archive":
      return "Изменено состояние архива"

    case "comment":
      return "Комментарий"

    case "attachment":
      return "Добавлено вложение"

    case "email":
      return "Отправлено письмо"

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

    case "status":
      return "↔"

    case "assign":
      return "👤"

    case "sla":
      return "⏱"

    case "priority":
      return "!"

    case "type":
      return "◆"

    case "archive":
      return "□"

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

function getDescription(
  item: TimelineItem
): string | null {
  const text = item.meta?.text

  if (typeof text === "string") {
    return text
  }

  const description = item.meta?.description

  if (typeof description === "string") {
    return description
  }

  return null
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
      !HIDDEN_FIELDS.has(field)
  )
}

function getTransitionChange(
  item: TimelineItem
): TimelineChange | null {
  const preferredFields =
    item.action === "status"
      ? ["status"]
      : [
          "executor",
          "executors",
          "assignee",
          "assignees",
          "assigned_to",
          "executor_group",
        ]

  for (const field of preferredFields) {
    const change = item.changes?.[field]

    if (change) {
      return change
    }
  }

  return getVisibleChanges(item)[0]?.[1] ?? null
}

function Changes({
  item,
}: {
  item: TimelineItem
}) {
  const changes = getVisibleChanges(item)

  if (!changes.length) {
    return null
  }

  return (
    <div className="ticket-timeline-changes">
      {changes.map(
        ([field, change]) => (
          <div
            key={field}
            className="ticket-timeline-change-row"
          >
            <div className="ticket-timeline-change-label">
              {change.label || field}
            </div>

            <div className="ticket-timeline-change-values">
              <span className="ticket-timeline-value-old">
                {formatValue(change.before)}
              </span>

              <span className="ticket-timeline-arrow">
                →
              </span>

              <span className="ticket-timeline-value-new">
                {formatValue(change.after)}
              </span>
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
  if (item.action !== "create") {
    return null
  }

  const changes = getVisibleChanges(item)

  if (!changes.length) {
    return (
      <div className="ticket-timeline-description">
        Заявка была создана.
      </div>
    )
  }

  return (
    <div className="ticket-timeline-create-summary">
      {changes.map(
        ([field, change]) => (
          <div
            key={field}
            className="ticket-timeline-create-row"
          >
            <span className="ticket-timeline-create-label">
              {change.label || field}
            </span>

            <span className="ticket-timeline-create-value">
              {formatValue(change.after)}
            </span>
          </div>
        )
      )}
    </div>
  )
}


// =========================================================
// EVENT BODY
// =========================================================

function EventBody({
  item,
}: {
  item: TimelineItem
}) {
  const description = getDescription(item)

  if (item.action === "comment") {
    return (
      <div className="ticket-timeline-comment">
        {description || "Комментарий без текста"}
      </div>
    )
  }

  if (
    item.action === "status" ||
    item.action === "assign"
  ) {
    const change = getTransitionChange(item)

    const from =
      item.meta?.from ??
      change?.before

    const to =
      item.meta?.to ??
      change?.after

    return (
      <div className="ticket-timeline-transition">
        <span>
          {formatValue(from)}
        </span>

        <span className="ticket-timeline-arrow">
          →
        </span>

        <span>
          {formatValue(to)}
        </span>
      </div>
    )
  }

  return (
    <>
      {description && (
        <div className="ticket-timeline-description">
          {description}
        </div>
      )}

      <CreateSummary item={item} />

      {item.action !== "create" && (
        <Changes item={item} />
      )}
    </>
  )
}


// =========================================================
// ENTRY
// =========================================================

function TimelineEntry({
  item,
  compact,
  isLast,
}: {
  item: TimelineItem
  compact: boolean
  isLast: boolean
}) {
  const className = [
    "ticket-timeline-row",
    compact
      ? "ticket-timeline-row-compact"
      : "",
    isLast
      ? "ticket-timeline-row-last"
      : "",
    `ticket-timeline-action-${item.action}`,
  ]
    .filter(Boolean)
    .join(" ")

  return (
    <div className={className}>
      <div className="ticket-timeline-rail">
        <div className="ticket-timeline-marker">
          {getActionIcon(item.action)}
        </div>
      </div>

      <div className="ticket-timeline-content">
        <div className="ticket-timeline-title">
          {getActionTitle(item)}
        </div>

        <div className="ticket-timeline-meta">
          <span>
            {item.actor?.label || "Система"}
          </span>

          {item.date && (
            <>
              <span className="ticket-timeline-dot">
                •
              </span>

              <span>
                {formatDate(item.date)}
              </span>
            </>
          )}
        </div>

        <EventBody item={item} />
      </div>
    </div>
  )
}


// =========================================================
// STATES
// =========================================================

function LoadingState() {
  return (
    <div className="ticket-timeline-state">
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
        "ticket-timeline-state",
        "ticket-timeline-error",
      ].join(" ")}
    >
      <div>{error}</div>

      <button
        type="button"
        onClick={reload}
        className="ticket-timeline-retry"
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
    <div className="ticket-timeline-state">
      {text}
    </div>
  )
}


// =========================================================
// CONTENT
// =========================================================

function TimelineContent({
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
    return <LoadingState />
  }

  if (error) {
    return (
      <ErrorState
        error={error}
        reload={reload}
      />
    )
  }

  const ordered = reverse
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
    <div className="ticket-timeline">
      {ordered.map(
        (
          item,
          index
        ) => {
          const day = formatDate(
            item.date,
            true
          )

          const previous =
            index > 0
              ? ordered[index - 1]
              : null

          const previousDay = previous
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
            <div
              key={item.id}
              className="ticket-timeline-group"
            >
              {showDay && (
                <div className="ticket-timeline-day">
                  {day}
                </div>
              )}

              <TimelineEntry
                item={item}
                compact={compact}
                isLast={
                  index === ordered.length - 1
                }
              />
            </div>
          )
        }
      )}
    </div>
  )
}


// =========================================================
// WIDGET
// =========================================================

export function TimelineWidget(
  props: WidgetProps
) {
  const ticketId = getTicketId(
    props.value
  )

  const config = useMemo(
    () => ({
      type: "timeline" as const,

      source: "ticket.history",

      params: {
        id: ticketId,
      },

      compact: false,
      reverse: false,
      groupByDate: true,
      emptyText: "Жизненный цикл пока пуст",
    }),
    [ticketId]
  )

  const viewModel = useTimelineController(
    config
  )

  if (!ticketId) {
    return (
      <BaseWidget
        field={props.field}
        loading={false}
      >
        <div className="ticket-timeline-state">
          История появится после создания заявки.
        </div>
      </BaseWidget>
    )
  }

  return (
    <BaseWidget
      field={props.field}
      loading={
        Boolean(props.loading) ||
        viewModel.loading
      }
    >
      <TimelineContent
        {...viewModel}
      />
    </BaseWidget>
  )
}