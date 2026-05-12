import { useState } from "react"
import { useTraceSession } from "./hooks"
import { getTraceHeadline, getTraceSubline } from "./format"
import { TracePanel } from "./TracePanel"

export function TraceBadge() {
  const session = useTraceSession()
  const [open, setOpen] = useState(false)

  const lastError = session.lastError
  const last = session.last

  /* ⭐ ничего нет */
  if (!lastError && !last) return null

  /* ⭐ есть только успешный trace */
  if (!lastError && last) {

    const record = last

    return (
      <>
        <button
          onClick={() => setOpen(true)}
          title="Открыть trace session"
          style={{
            position: "fixed",
            right: 16,
            bottom: 16,
            zIndex: 10000,
            borderRadius: 999,
            border: "1px solid #cbd5e1",
            background: "#eff6ff",
            color: "#1e3a8a",
            padding: "8px 12px",
            boxShadow: "0 8px 24px rgba(0,0,0,0.12)",
            cursor: "pointer",
            touchAction: "manipulation",
          }}
        >
          ✔ {getTraceHeadline(record)}
        </button>

        <TracePanel open={open} onClose={() => setOpen(false)} />
      </>
    )
  }

  /* ⭐ есть ошибка */
  if (lastError) {

    const record = lastError

    return (
      <>
        <button
          onClick={() => setOpen(true)}
          style={{
            position: "fixed",
            right: 16,
            bottom: 16,
            zIndex: 10000,
            maxWidth: 420,
            width: "calc(100vw - 24px)",
            borderRadius: 14,
            border: "1px solid #f1c0c0",
            background: "#fff5f5",
            color: "#7f1d1d",
            padding: 12,
            boxShadow: "0 8px 24px rgba(0,0,0,0.12)",
            cursor: "pointer",
            textAlign: "left",
            touchAction: "manipulation",
          }}
        >
          <div style={{ fontWeight: 700, marginBottom: 4 }}>
            ⚠ {getTraceHeadline(record)}
          </div>

          <div style={{ fontSize: 12, opacity: 0.9 }}>
            {getTraceSubline(record)}
          </div>

          <div style={{ fontSize: 12, marginTop: 6, opacity: 0.8 }}>
            Ошибок в сессии: {session.errors.length} · нажми чтобы размотать
          </div>
        </button>

        <TracePanel open={open} onClose={() => setOpen(false)} />
      </>
    )
  }

  return null
}