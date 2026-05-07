import { useSyncExternalStore } from "react"
import { traceSessionStore } from "./TraceSessionStore"
import type { TraceSessionState } from "./TraceSessionStore"

export function useTraceSession(): TraceSessionState {
  return useSyncExternalStore(
    traceSessionStore.subscribe.bind(traceSessionStore),
    traceSessionStore.getSnapshot.bind(traceSessionStore),
    traceSessionStore.getSnapshot.bind(traceSessionStore),
  )
}