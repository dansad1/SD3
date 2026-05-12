import type { TraceRecord, TraceStep } from "./types"

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

export function buildHumanSummary(record: TraceRecord): string {

  const failed = findDeepestError(record.root)

  /* =========================================
     OK REQUEST
  ========================================= */

  if (!failed && record.trigger === "request") {

    const api = record.root.meta?.api
    const method = record.root.meta?.method

    if (api) {
      return `${method || "GET"} ${api}`
    }

    return "API request completed"
  }

  /* =========================================
     FAILED PATH
  ========================================= */

  if (failed) {

    const meta = failed.meta || {}

    /* ---------- API ERROR ---------- */

    if (meta.api) {

      const method = meta.method || "GET"
      const status = meta.status

      if (status) {
        return `${method} ${meta.api} → ${status}`
      }

      return `${method} ${meta.api} failed`
    }

    /* ---------- ACTION ERROR ---------- */

    if (meta.action) {

      if (meta.status) {
        return `Action ${meta.action} → ${meta.status}`
      }

      return `Action ${meta.action} failed`
    }

    /* ---------- ENTITY FORM ERROR ---------- */

    if (meta.entity) {

      const mode = meta.mode

      if (mode) {
        return `${meta.entity} ${mode} failed`
      }

      return `${meta.entity} operation failed`
    }

    /* ---------- RENDER ERROR ---------- */

    if (meta.block) {
      return `Render failed in ${meta.block}`
    }

    if (meta.stage) {
      return `Stage "${meta.stage}" failed`
    }

    /* ---------- GENERIC ERROR ---------- */

    if (meta.error) {
      return String(meta.error).slice(0, 120)
    }

    return "Operation failed"
  }

  /* =========================================
     OK ACTION
  ========================================= */

  if (record.trigger === "action") {

    const action = record.root.meta?.action

    if (action) {
      return `Action ${action} completed`
    }

    return "Action completed"
  }

  /* =========================================
     OK MOUNT
  ========================================= */

  if (record.trigger === "mount") {
    return `Page ${record.page} mounted`
  }

  return record.summary || "Trace event"
}