import type { TraceMeta, TraceRecord, TraceStep } from "./types"

/* =========================================================
   TIME / ID
========================================================= */

export function traceNow(): number {
  return performance.now()
}

export function traceId(prefix = "tr"): string {
  const part = Math.random().toString(36).slice(2, 8)
  return `${prefix}_${Date.now().toString(36)}_${part}`
}

/* =========================================================
   ERROR STACK NORMALIZATION ⭐⭐⭐
========================================================= */

function extractUsefulStack(stack?: string): string {

  if (!stack) return ""

  const lines = stack.split("\n")

  const useful = lines.filter(line =>
    line.includes("/src/") &&
    !line.includes("node_modules") &&
    !line.includes("react-dom") &&
    !line.includes("react-router") &&
    !line.includes("FrameworkErrorBoundary") &&
    !line.includes("BrowserRouter")
  )

  return useful.slice(0, 6).join("\n")
}

export function normalizeError(error: unknown): string {

  if (!error) return "Unknown error"

  if (error instanceof Error) {

    const focused = extractUsefulStack(error.stack)

    if (focused) {
      return `${error.message}\n${focused}`
    }

    return error.message || String(error)
  }

  if (typeof error === "string") {
    return error
  }

  try {
    return JSON.stringify(error, null, 2)
  } catch {
    return String(error)
  }
}

/* =========================================================
   DURATIONS
========================================================= */

export function stepDuration(step: TraceStep): number | null {
  if (typeof step.finishedAt !== "number") return null
  return Math.max(0, step.finishedAt - step.startedAt)
}

export function recordDuration(record: TraceRecord): number {
  return Math.max(0, record.finishedAt - record.startedAt)
}

/* =========================================================
   ERROR SEARCH
========================================================= */

export function findFirstError(step: TraceStep): TraceStep | undefined {

  if (step.status === "error") return step

  for (const child of step.children) {
    const found = findFirstError(child)
    if (found) return found
  }

  return undefined
}

export function findDeepestError(step: TraceStep): TraceStep | undefined {

  let result: TraceStep | undefined

  function walk(node: TraceStep) {
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

/* =========================================================
   HUMAN SUMMARY ⭐⭐⭐
========================================================= */

export function buildSummary(record: TraceRecord): string {

  const failed =
    findDeepestError(record.root) ||
    findFirstError(record.root)

  /* ---------- OK REQUEST ---------- */

  if (!failed && record.trigger === "request") {

    const meta = record.root.meta || {}

    if (meta.api) {
      const method = meta.method || "GET"
      return `${method} ${meta.api}`
    }

    return `Request OK`
  }

  /* ---------- FAILED ---------- */

  if (failed) {

    const meta = failed.meta || {}

    /* API */

    if (meta.api) {

      const method = meta.method || "GET"
      const status = meta.status

      if (status) {
        return `${method} ${meta.api} → ${status}`
      }

      return `${method} ${meta.api} failed`
    }

    /* ACTION */

    if (meta.action) {

      if (meta.status) {
        return `Action ${meta.action} → ${meta.status}`
      }

      return `Action ${meta.action} failed`
    }

    /* ENTITY */

    if (meta.entity) {

      if (meta.mode) {
        return `${meta.entity} ${meta.mode} failed`
      }

      return `${meta.entity} operation failed`
    }

    /* BLOCK */

    if (meta.block) {
      return `Render failed in ${meta.block}`
    }

    /* STAGE */

    if (meta.stage) {
      return `Stage "${meta.stage}" failed`
    }

    /* GENERIC */

    if (meta.error) {
      return String(meta.error).slice(0, 140)
    }

    return `${record.page} failed`
  }

  /* ---------- OK ACTION ---------- */

  if (record.trigger === "action") {

    const action = record.root.meta?.action

    if (action) {
      return `Action ${action} completed`
    }

    return `Action completed`
  }

  /* ---------- OK MOUNT ---------- */

  if (record.trigger === "mount") {
    return `Page ${record.page} mounted`
  }

  return `${record.page} / ${record.trigger}`
}

/* =========================================================
   META MERGE
========================================================= */

export function mergeMeta(
  base?: TraceMeta,
  patch?: TraceMeta
): TraceMeta | undefined {

  if (!base && !patch) return undefined

  return {
    ...(base || {}),
    ...(patch || {}),
  }
}

/* =========================================================
   TIME AGO
========================================================= */

export function humanTimeAgo(ts: number): string {

  const delta = Date.now() - ts

  if (delta < 5_000) return "только что"
  if (delta < 60_000) return `${Math.floor(delta / 1000)}с назад`
  if (delta < 3_600_000) return `${Math.floor(delta / 60_000)}м назад`

  return `${Math.floor(delta / 3_600_000)}ч назад`
}