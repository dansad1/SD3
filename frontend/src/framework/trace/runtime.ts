import { TraceEngine } from "./TraceEngine"
import { traceSessionStore } from "./TraceSessionStore"
import type { TraceMeta, TraceRecord, TraceTrigger } from "./types"

class TraceRuntime {

  private active?: TraceEngine

  /* =====================================================
     CURRENT
  ===================================================== */

  current(): TraceEngine | undefined {
    return this.active
  }

  /* =====================================================
     START ROOT TRACE
  ===================================================== */

  start(params: {
    page: string
    trigger: TraceTrigger
    rootName?: string
    meta?: TraceMeta
  }): TraceEngine {

    // ⭐ если предыдущий trace не закрыт — закрываем
    if (this.active && !this.active.isClosed()) {

      const record = this.active.finishError(
        new Error("Trace interrupted"),
        { stage: "runtime_interrupt" }
      )

      traceSessionStore.push(record)
    }

    const trace = new TraceEngine(params)
    this.active = trace

    return trace
  }

  /* =====================================================
     ENSURE ROOT
  ===================================================== */

  ensureRoot(params: {
    page: string
    trigger: TraceTrigger
    rootName?: string
    meta?: TraceMeta
  }): TraceEngine {

    if (this.active && !this.active.isClosed()) {
      return this.active
    }

    return this.start(params)
  }

  /* =====================================================
     FINISH
  ===================================================== */

  finishOk(meta?: TraceMeta): TraceRecord | undefined {

    if (!this.active) return

    const current = this.active
    const record = current.finishOk(meta)

    if (this.active === current) {
      this.active = undefined
    }

    if (record) {
      traceSessionStore.push(record)
    }

    return record
  }

  finishError(error: unknown, meta?: TraceMeta): TraceRecord | undefined {

    if (!this.active) return

    const current = this.active
    const record = current.finishError(error, meta)

    if (this.active === current) {
      this.active = undefined
    }

    if (record) {
      traceSessionStore.push(record)
    }

    return record
  }

  /* =====================================================
     RUN ROOT OR STEP ⭐⭐⭐
  ===================================================== */

  async run<T>(
    params: {
      page: string
      trigger: TraceTrigger
      rootName?: string
      meta?: TraceMeta
    },
    fn: (trace: TraceEngine) => Promise<T> | T
  ): Promise<T> {

    // ⭐ если уже есть trace → просто step
    if (this.active && !this.active.isClosed()) {

      return this.active.step(
        params.rootName || params.trigger,
        () => fn(this.active!),
        params.meta
      )
    }

    const trace = this.start(params)

    try {
      const result = await fn(trace)
      this.finishOk()
      return result
    } catch (error) {
      this.finishError(error)
      throw error
    }
  }

  /* =====================================================
     MANUAL STEP API (очень удобно)
  ===================================================== */

  stepSync<T>(name: string, fn: () => T, meta?: TraceMeta): T {

    const trace = this.active
    if (!trace) return fn()

    return trace.stepSync(name, fn, meta)
  }

  async step<T>(
    name: string,
    fn: () => Promise<T> | T,
    meta?: TraceMeta
  ): Promise<T> {

    const trace = this.active
    if (!trace) return fn()

    return trace.step(name, fn, meta)
  }

  /* =====================================================
     RESET (navigation safe)
  ===================================================== */

  resetActive() {
    this.active = undefined
  }
}

export const traceRuntime = new TraceRuntime()