import { useEffect, useState } from "react"
import { TracePanel } from "@/framework/trace/TracePanel"
import { traceSessionStore } from "@/framework/trace/TraceSessionStore"

export function DevToolsRoot() {

  const [open, setOpen] = useState(
    () => localStorage.getItem("trace_open") === "1"
  )

  /* =====================================================
     PERSIST STATE
  ===================================================== */

  useEffect(() => {
    localStorage.setItem("trace_open", open ? "1" : "0")
  }, [open])

  /* =====================================================
     HOTKEY
  ===================================================== */

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {

      if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "t") {
        setOpen(v => !v)
      }

    }

    window.addEventListener("keydown", handler)
    return () => window.removeEventListener("keydown", handler)

  }, [])

  /* =====================================================
     GLOBAL JS ERRORS
  ===================================================== */

  useEffect(() => {

    const onError = (event: ErrorEvent) => {

      traceSessionStore.push({
        id: crypto.randomUUID(),
        page: window.location.pathname,
        trigger: "mount",
        status: "error",
        startedAt: Date.now(),
        finishedAt: Date.now(),
        summary: "Global runtime error",
        root: {
          id: crypto.randomUUID(),
          name: "window_error",
          status: "error",
          startedAt: Date.now(),
          finishedAt: Date.now(),
          meta: {
            message: event.message,
            file: event.filename,
            line: event.lineno,
            column: event.colno,
          },
          children: [],
        },
      })

      setOpen(true)

    }

    const onRejection = (event: PromiseRejectionEvent) => {

      const reason = event.reason

      traceSessionStore.push({
        id: crypto.randomUUID(),
        page: window.location.pathname,
        trigger: "mount",
        status: "error",
        startedAt: Date.now(),
        finishedAt: Date.now(),
        summary: "Unhandled promise rejection",
        root: {
          id: crypto.randomUUID(),
          name: "promise_rejection",
          status: "error",
          startedAt: Date.now(),
          finishedAt: Date.now(),
          meta: {
            error:
              reason instanceof Error
                ? reason.message
                : String(reason),
          },
          children: [],
        },
      })

      setOpen(true)

    }

    window.addEventListener("error", onError)
    window.addEventListener("unhandledrejection", onRejection)

    return () => {
      window.removeEventListener("error", onError)
      window.removeEventListener("unhandledrejection", onRejection)
    }

  }, [])

  /* =====================================================
     UI
  ===================================================== */

  return (
    <>
      {/* FLOAT BUTTON */}
      <button
        onClick={() => setOpen(v => !v)}
        style={{
          position: "fixed",
          right: 16,
          bottom: 16,
          zIndex: 999999,
          padding: "10px 14px",
          borderRadius: 12,
          border: "1px solid #e5e7eb",
          background: "#111827",
          color: "#fff",
          cursor: "pointer",
          fontSize: 12,
        }}
      >
        TRACE
      </button>

      <TracePanel
        open={open}
        onClose={() => setOpen(false)}
      />
    </>
  )
}