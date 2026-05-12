import type {
  TraceMeta,
  TraceRecord,
  TraceStep,
  TraceTrigger,
} from "./types"

import {
  mergeMeta,
  normalizeError,
  traceId,
  traceNow,
} from "./utils"

import { buildHumanSummary } from "./buildHumanSummary"

type StartParams = {
  page: string
  trigger: TraceTrigger
  rootName?: string
  meta?: TraceMeta
}

export class TraceEngine {
  readonly id: string
  readonly page: string
  readonly trigger: TraceTrigger
  readonly startedAt: number

  private rootStep: TraceStep
  private stack: TraceStep[]
  private closed = false

  constructor(params: StartParams) {
    this.id = traceId("trace")
    this.page = params.page
    this.trigger = params.trigger
    this.startedAt = Date.now()

    this.rootStep = {
      id: traceId("step"),
      name: params.rootName || `${params.page}:${params.trigger}`,
      status: "running",
      meta: mergeMeta(
        { page: params.page },
        params.meta
      ),
      startedAt: traceNow(),
      children: [],
    }

    this.stack = [this.rootStep]
  }

  get root(): TraceStep {
    return this.rootStep
  }

  get current(): TraceStep {
    return this.stack[this.stack.length - 1]
  }

  isClosed(): boolean {
    return this.closed
  }

  annotate(meta: TraceMeta) {
    if (this.closed) return
    this.current.meta = mergeMeta(this.current.meta, meta)
  }

  enter(name: string, meta?: TraceMeta): TraceStep {
    if (this.closed) {
      throw new Error("TraceEngine is already closed")
    }

    const parent = this.current

    const step: TraceStep = {
      id: traceId("step"),
      name,
      status: "running",
      meta,
      startedAt: traceNow(),
      children: [],
    }

    parent.children.push(step)
    this.stack.push(step)

    return step
  }

  leaveOk(meta?: TraceMeta) {
    if (this.closed) return

    const step = this.stack.pop()
    if (!step) return

    step.meta = mergeMeta(step.meta, meta)
    step.status = "ok"
    step.finishedAt = traceNow()

    if (this.stack.length === 0) {
      this.stack = [this.rootStep]
    }
  }

  leaveError(error: unknown, meta?: TraceMeta) {
    if (this.closed) return

    const step = this.stack.pop()
    if (!step) return

    step.meta = mergeMeta(step.meta, {
      ...meta,
      error: normalizeError(error),
    })

    step.status = "error"
    step.finishedAt = traceNow()

    if (this.stack.length === 0) {
      this.stack = [this.rootStep]
    }
  }

  stepSync<T>(
    name: string,
    fn: () => T,
    meta?: TraceMeta
  ): T {
    this.enter(name, meta)

    try {
      const result = fn()
      this.leaveOk()
      return result
    } catch (error) {
      this.leaveError(error)
      throw error
    }
  }

  async step<T>(
    name: string,
    fn: () => Promise<T> | T,
    meta?: TraceMeta
  ): Promise<T> {
    this.enter(name, meta)

    try {
      const result = await fn()
      this.leaveOk()
      return result
    } catch (error) {
      this.leaveError(error)
      throw error
    }
  }

  finishOk(meta?: TraceMeta): TraceRecord {
    return this.finish("ok", undefined, meta)
  }

  finishError(error: unknown, meta?: TraceMeta): TraceRecord {
    return this.finish("error", error, meta)
  }

  private finish(
    status: "ok" | "error",
    error?: unknown,
    meta?: TraceMeta
  ): TraceRecord {

    if (this.closed) {
      throw new Error("TraceEngine is already closed")
    }

    this.closed = true

    /* ================================
       CLOSE ALL DANGLING STEPS
    ================================ */

    while (this.stack.length > 1) {

      const dangling = this.stack.pop()
      if (!dangling) break

      dangling.status = status
      dangling.meta = mergeMeta(dangling.meta, meta)

      if (error && status === "error") {
        dangling.meta = mergeMeta(dangling.meta, {
          error: normalizeError(error),
        })
      }

      dangling.finishedAt = traceNow()
    }

    /* ================================
       CLOSE ROOT
    ================================ */

    this.rootStep.status = status
    this.rootStep.meta = mergeMeta(this.rootStep.meta, meta)

    if (error && status === "error") {
      this.rootStep.meta = mergeMeta(this.rootStep.meta, {
        error: normalizeError(error),
      })
    }

    this.rootStep.finishedAt = traceNow()

    /* ================================
       BUILD RECORD
    ================================ */

    const record: TraceRecord = {
      id: this.id,
      page: this.page,
      trigger: this.trigger,
      status,
      startedAt: this.startedAt,
      finishedAt: Date.now(),
      root: this.rootStep,
      summary: "",
    }

    /* ⭐ HUMAN SUMMARY */

    record.summary = buildHumanSummary(record)

    return record
  }
}