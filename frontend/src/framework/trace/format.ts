import type { TraceRecord, TraceStep } from "./types"
import { findDeepestError } from "./utils"

export function getTraceHeadline(record: TraceRecord): string {
  if (record.status === "ok") {
    return `${record.page} / ${record.trigger}`
  }

  const failed = findDeepestError(record.root)
  if (!failed) {
    return `${record.page} / ошибка`
  }

  return `${record.page} / ${failed.name}`
}

export function getTraceSubline(record: TraceRecord): string {
  const failed = findDeepestError(record.root)

  if (!failed) {
    return record.summary
  }

  const parts = [
    failed.meta?.entity,
    failed.meta?.field,
    failed.meta?.action,
    failed.meta?.api,
  ].filter(Boolean)

  return parts.join(" / ") || record.summary
}

export function getStepLabel(step: TraceStep): string {
  const bits = [step.name]

  if (step.meta?.entity) bits.push(`entity=${step.meta.entity}`)
  if (step.meta?.field) bits.push(`field=${step.meta.field}`)
  if (step.meta?.action) bits.push(`action=${step.meta.action}`)
  if (step.meta?.api) bits.push(`api=${step.meta.api}`)

  return bits.join(" · ")
}