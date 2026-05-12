import { resolveProps } from "@/framework/bind/expression/resolveProps"
import type { PageRuntimeContext } from "@/framework/bind/types"
import { buildBindScope } from "../scope/bindScope"

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value)
}

/**
 * Делаем безопасный plain snapshot, чтобы:
 * - не зависеть от мутаций feature pipeline
 * - не таскать prototype / class instances
 */
export function toPlainSnapshot<T>(value: T): T {
  if (Array.isArray(value)) {
    return value.map(item => toPlainSnapshot(item)) as T
  }

  if (isPlainObject(value)) {
    const out: Record<string, unknown> = {}

    for (const [k, v] of Object.entries(value)) {
      out[k] = toPlainSnapshot(v)
    }

    return out as T
  }

  return value
}

function stableSortObject(
  value: unknown
): unknown {
  if (Array.isArray(value)) {
    return value.map(stableSortObject)
  }

  if (isPlainObject(value)) {
    const out: Record<string, unknown> = {}

    for (const key of Object.keys(value).sort()) {
      out[key] = stableSortObject(value[key])
    }

    return out
  }

  return value
}

export function stableStringify(value: unknown): string {
  return JSON.stringify(stableSortObject(value))
}

export function resolveWithContext<T extends Record<string, unknown>>(
  props: T,
  ctx: PageRuntimeContext
): T {
  const snapshot = toPlainSnapshot(props)
  const scope = buildBindScope(ctx)

  return resolveProps(snapshot, scope) as T
}