import type { TraceRecord, TraceSnapshot } from "./types"

type Listener = () => void
type TraceFilterMode = "errors" | "all"

export type TraceSessionState = {
  records: TraceRecord[]
  errors: TraceRecord[]
  last?: TraceRecord
  lastError?: TraceRecord
  errorCount: number
  mode: TraceFilterMode
}

export class TraceSessionStore {

  private records: TraceRecord[] = []
  private listeners = new Set<Listener>()
  private readonly maxSize: number
  private mode: TraceFilterMode = "errors"

  private snapshot: TraceSnapshot & TraceSessionState = {
    records: [],
    errors: [],
    last: undefined,
    lastError: undefined,
    errorCount: 0,
    mode: "errors",
  }

  constructor(maxSize = 50) {
    this.maxSize = maxSize
  }

  /* =====================================================
     SUBSCRIBE
  ===================================================== */

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  /* =====================================================
     INTERNAL HELPERS
  ===================================================== */

  private rebuildSnapshot() {

    const all = this.records

    const errors = all.filter(r => r.status === "error")

    const visible =
      this.mode === "all"
        ? all
        : errors

    this.snapshot = {
      records: visible,
      errors,
      last: all.length > 0 ? all[0] : undefined,
      lastError: errors.length > 0 ? errors[0] : undefined,
      errorCount: errors.length,
      mode: this.mode,
    }
  }

  private emit() {
    this.rebuildSnapshot()
    this.listeners.forEach(l => l())
  }

  private isDuplicate(a: TraceRecord, b: TraceRecord): boolean {
    return (
      a.page === b.page &&
      a.trigger === b.trigger &&
      a.summary === b.summary &&
      Math.abs(a.finishedAt - b.finishedAt) < 300
    )
  }

  /* =====================================================
     PUBLIC API
  ===================================================== */

  push(record: TraceRecord) {

    const prev = this.records[0]

    // 🔥 dedupe быстрых одинаковых trace
    if (prev && this.isDuplicate(prev, record)) {
      this.records[0] = record
    } else {
      this.records.unshift(record)
    }

    if (this.records.length > this.maxSize) {
      this.records.length = this.maxSize
    }

    this.emit()
  }

  clear() {
    this.records = []
    this.emit()
  }

  setMode(mode: TraceFilterMode) {
    if (this.mode === mode) return
    this.mode = mode
    this.emit()
  }

  getSnapshot(): TraceSnapshot & TraceSessionState {
    return this.snapshot
  }
}

export const traceSessionStore = new TraceSessionStore(60)