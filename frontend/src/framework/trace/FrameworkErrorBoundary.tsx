import React from "react"
import { traceRuntime } from "./runtime"
import { traceSessionStore } from "./TraceSessionStore"

type State = {
  error?: Error
}

function pushFallbackCrash(
  error: Error,
  extra?: Record<string, unknown>
) {
  traceSessionStore.push({
    id: crypto.randomUUID(),
    page: window.location.pathname,
    trigger: "mount",
    status: "error",
    startedAt: Date.now(),
    finishedAt: Date.now(),
    summary: error.message,
    root: {
      id: crypto.randomUUID(),
      name: "react_render_crash",
      status: "error",
      startedAt: Date.now(),
      finishedAt: Date.now(),
      meta: {
        error: error.message,
        ...extra,
      },
      children: [],
    },
  })
}

export class FrameworkErrorBoundary extends React.Component<
  { children: React.ReactNode },
  State
> {
  state: State = {}

  static getDerivedStateFromError(error: Error) {
    return { error }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    const active = traceRuntime.current()

    if (active && !active.isClosed()) {
      traceRuntime.finishError(error, {
        stage: "react_render",
        stack: info.componentStack,
      })
    } else {
      pushFallbackCrash(error, {
        stage: "react_render",
        stack: info.componentStack,
      })
    }

    console.error("Framework crash:", error, info)
  }

  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 40 }}>
          <h2>UI runtime crash</h2>

          <pre style={{ whiteSpace: "pre-wrap" }}>
            {this.state.error.message}
          </pre>

          <button
            style={{ marginTop: 20 }}
            onClick={() => this.setState({ error: undefined })}
          >
            Попробовать восстановить UI
          </button>
        </div>
      )
    }

    return this.props.children
  }
}