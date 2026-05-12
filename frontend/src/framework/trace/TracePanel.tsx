import { useMemo, useState } from "react"
import type { TraceRecord, TraceStep } from "./types"
import { useTraceSession } from "./hooks"
import { traceSessionStore } from "./TraceSessionStore"
import { stepDuration, recordDuration, humanTimeAgo } from "./utils"

function StatusDot({
  status,
}: {
  status: "running" | "ok" | "error"
}) {
  const color =
    status === "ok"
      ? "#15803d"
      : status === "error"
      ? "#b91c1c"
      : "#a16207"

  return (
    <span
      style={{
        width: 10,
        height: 10,
        borderRadius: "50%",
        background: color,
        display: "inline-block",
        flex: "0 0 auto",
      }}
    />
  )
}

function buildHeadline(record: TraceRecord): string {
  return `${record.page} / ${record.trigger}`
}

function buildSubline(record: TraceRecord): string {
  const failed = findDeepestError(record.root)

  if (!failed) {
    return record.summary
  }

  const parts = [
    failed.name,
    failed.meta?.entity,
    failed.meta?.field,
    failed.meta?.action,
  ].filter(Boolean)

  return parts.join(" / ")
}

function findDeepestError(step: TraceStep): TraceStep | undefined {
  let result: TraceStep | undefined

  const walk = (node: TraceStep) => {
    if (node.status === "error") {
      result = node
    }

    for (const child of node.children) {
      walk(child)
    }
  }

  walk(step)
  return result
}

function StepRow({
  step,
  depth = 0,
}: {
  step: TraceStep
  depth?: number
}) {

  const hasChildren = step.children.length > 0
  const hasMeta = !!step.meta && Object.keys(step.meta).length > 0

  const canOpen = hasChildren || hasMeta

  const [open, setOpen] = useState(depth < 1)

  const duration = stepDuration(step)

  return (
    <div style={{ marginLeft: depth * 14 }}>

      <div
        onClick={() => canOpen && setOpen(v => !v)}
        style={{
          display: "flex",
          alignItems: "center",
          gap: 8,
          padding: "5px 0",
          cursor: canOpen ? "pointer" : "default",
          fontSize: 13,
        }}
      >
        <StatusDot status={step.status} />
        <span style={{ fontWeight: 600 }}>{step.name}</span>

        <span style={{ marginLeft: "auto", opacity: 0.65, fontSize: 12 }}>
          {typeof duration === "number"
            ? `${Math.round(duration)}ms`
            : ""}
        </span>
      </div>

      {/* ⭐ meta inspector */}

      {open && hasMeta && (
        <div
          style={{
            marginLeft: 18,
            marginBottom: 8,
            padding: 8,
            borderRadius: 8,
            background: "#f8fafc",
            border: "1px solid #e2e8f0",
            fontSize: 12,
            whiteSpace: "pre-wrap",
            wordBreak: "break-word",
          }}
        >
          {JSON.stringify(step.meta, null, 2)}
        </div>
      )}

      {/* ⭐ children */}

      {open && hasChildren && (
        <div>
          {step.children.map(child => (
            <StepRow
              key={child.id}
              step={child}
              depth={depth + 1}
            />
          ))}
        </div>
      )}

    </div>
  )
}

function RecordView({
  record,
}: {
  record: TraceRecord
}) {
  return (
    <div>
      <div style={{ marginBottom: 12 }}>
        <div style={{ fontSize: 18, fontWeight: 700 }}>
          {buildHeadline(record)}
        </div>

        <div style={{ fontSize: 12, opacity: 0.7, marginTop: 4 }}>
          {record.status} · {humanTimeAgo(record.finishedAt)} ·{" "}
          {Math.round(recordDuration(record))}ms
        </div>

        <div style={{ fontSize: 13, opacity: 0.85, marginTop: 6 }}>
          {buildSubline(record)}
        </div>
      </div>

      <StepRow step={record.root} />
    </div>
  )
}

export function TracePanel({
  open,
  onClose,
}: {
  open: boolean
  onClose: () => void
}) {
  const session = useTraceSession()
  const [selectedId, setSelectedId] = useState<string | undefined>()

  const selected = useMemo(() => {
    if (!selectedId) return session.records[0]
    return session.records.find(r => r.id === selectedId) || session.records[0]
  }, [selectedId, session.records])

  if (!open) return null

  return (
    <div
      style={{
        position: "fixed",
        right: 16,
        bottom: 72,
        width: "min(980px, calc(100vw - 24px))",
        height: "min(78vh, 760px)",
        background: "#fff",
        border: "1px solid #e5e7eb",
        borderRadius: 16,
        boxShadow: "0 16px 48px rgba(0,0,0,0.18)",
        display: "grid",
        gridTemplateColumns: "320px 1fr",
        overflow: "hidden",
        zIndex: 10001,
      }}
    >
      <div
        style={{
          borderRight: "1px solid #e5e7eb",
          display: "flex",
          flexDirection: "column",
          minHeight: 0,
        }}
      >
        <div
          style={{
            padding: 12,
            borderBottom: "1px solid #e5e7eb",
            display: "flex",
            flexDirection: "column",
            gap: 10,
          }}
        >
          <div>
            <div style={{ fontWeight: 700 }}>Trace session</div>
            <div style={{ fontSize: 12, opacity: 0.7 }}>
              ошибок: {session.errorCount}
            </div>
          </div>

          <div style={{ display: "flex", gap: 8 }}>
            <button
              onClick={() => traceSessionStore.setMode("errors")}
              style={{
                padding: "6px 10px",
                borderRadius: 8,
                border: "1px solid #d1d5db",
                background: session.mode === "errors" ? "#fee2e2" : "#fff",
                cursor: "pointer",
              }}
            >
              errors
            </button>

            <button
              onClick={() => traceSessionStore.setMode("all")}
              style={{
                padding: "6px 10px",
                borderRadius: 8,
                border: "1px solid #d1d5db",
                background: session.mode === "all" ? "#dbeafe" : "#fff",
                cursor: "pointer",
              }}
            >
              all
            </button>

            <button
              onClick={() => traceSessionStore.clear()}
              style={{
                marginLeft: "auto",
                padding: "6px 10px",
                borderRadius: 8,
                border: "1px solid #d1d5db",
                background: "#fff",
                cursor: "pointer",
              }}
            >
              очистить
            </button>
          </div>
        </div>

        <div
          style={{
            overflow: "auto",
            padding: 8,
            display: "flex",
            flexDirection: "column",
            gap: 8,
          }}
        >
          {session.records.length === 0 && (
            <div style={{ padding: 12, opacity: 0.65 }}>
              Нет trace для текущего фильтра
            </div>
          )}

          {session.records.map(record => (
            <button
              key={record.id}
              onClick={() => setSelectedId(record.id)}
              style={{
                textAlign: "left",
                border: selected?.id === record.id
                  ? "1px solid #8b5cf6"
                  : "1px solid #e5e7eb",
                background: selected?.id === record.id
                  ? "#f5f3ff"
                  : "#fff",
                borderRadius: 10,
                padding: 10,
                cursor: "pointer",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  marginBottom: 6,
                }}
              >
                <StatusDot status={record.status} />
                <strong style={{ fontSize: 13 }}>
                  {buildHeadline(record)}
                </strong>
              </div>

              <div style={{ fontSize: 12, opacity: 0.7 }}>
                {record.trigger} · {humanTimeAgo(record.finishedAt)} ·{" "}
                {Math.round(recordDuration(record))}ms
              </div>

              <div style={{ fontSize: 12, opacity: 0.9, marginTop: 6 }}>
                {buildSubline(record)}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div
        style={{
          padding: 14,
          overflow: "auto",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            gap: 8,
            marginBottom: 12,
          }}
        >
          <div style={{ fontWeight: 700 }}>Детали</div>
          <button
            onClick={onClose}
            style={{
              padding: "6px 10px",
              borderRadius: 8,
              border: "1px solid #d1d5db",
              background: "#fff",
              cursor: "pointer",
            }}
          >
            Закрыть
          </button>
        </div>

        {selected ? (
          <RecordView record={selected} />
        ) : (
          <div style={{ opacity: 0.65 }}>Нет выбранного trace</div>
        )}
      </div>
    </div>
  )
}