import { useEffect } from "react"
import { traceRuntime } from "@/framework/trace/runtime"
import { traceSessionStore } from "@/framework/trace/TraceSessionStore"

function pushFallbackCrash(
  message: string,
  extra?: Record<string, unknown>
) {
  traceSessionStore.push({
    id: crypto.randomUUID(),
    page: window.location.pathname,
    trigger: "mount",
    status: "error",
    startedAt: Date.now(),
    finishedAt: Date.now(),
    summary: message,
    root: {
      id: crypto.randomUUID(),
      name: "app_crash",
      status: "error",
      startedAt: Date.now(),
      finishedAt: Date.now(),
      meta: {
        error: message,
        ...extra,
      },
      children: [],
    },
  })
}

function reportCrash(
  error: unknown,
  extra?: Record<string, unknown>
) {
  const active = traceRuntime.current()

  if (active && !active.isClosed()) {
    traceRuntime.finishError(error, {
      stage: "global_runtime",
      ...extra,
    })
    return
  }

  const message =
    error instanceof Error
      ? error.message
      : typeof error === "string"
      ? error
      : String(error)

  pushFallbackCrash(message, extra)
}

export function AppCrashBridge() {
  useEffect(() => {
    const onError = (event: ErrorEvent) => {
      reportCrash(event.error || event.message, {
        type: "window_error",
        file: event.filename,
        line: event.lineno,
        column: event.colno,
      })
    }

    const onReject = (event: PromiseRejectionEvent) => {
      reportCrash(event.reason, {
        type: "promise_rejection",
      })
    }

    window.addEventListener("error", onError)
    window.addEventListener("unhandledrejection", onReject)

    return () => {
      window.removeEventListener("error", onError)
      window.removeEventListener("unhandledrejection", onReject)
    }
  }, [])

  return null
}