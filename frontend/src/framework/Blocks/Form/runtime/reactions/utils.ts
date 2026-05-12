import type { FormValues, MatchRule } from "./types"

export function getByPath<T = unknown>(
  obj: unknown,
  path: string
): T {
  return path.split(".").reduce<unknown>((acc, key) => {
    if (acc === null || acc === undefined) return undefined
    if (typeof acc !== "object") return undefined
    return (acc as Record<string, unknown>)[key]
  }, obj) as T
}

function isEmpty(value: unknown): boolean {
  return (
    value === null ||
    value === undefined ||
    value === "" ||
    (Array.isArray(value) && value.length === 0)
  )
}

export function matchRule(
  rule: MatchRule | undefined,
  values: FormValues
): boolean {
  if (!rule) return true

  if ("all" in rule) {
    return rule.all.every(r => matchRule(r, values))
  }

  if ("any" in rule) {
    return rule.any.some(r => matchRule(r, values))
  }

  if ("not" in rule) {
    return !matchRule(rule.not, values)
  }

  const value = values[rule.field]

  if ("empty" in rule && rule.empty !== undefined) {
    return isEmpty(value) === rule.empty
  }

  if ("eq" in rule) {
    return value === rule.eq
  }

  if ("neq" in rule) {
    return value !== rule.neq
  }

  if ("in" in rule && rule.in) {
    return rule.in.includes(value)
  }

  if ("notIn" in rule && rule.notIn) {
    return !rule.notIn.includes(value)
  }

  return true
}

export function shallowChangedFields(
  prev: FormValues,
  next: FormValues
): string[] {
  const keys = new Set([
    ...Object.keys(prev),
    ...Object.keys(next),
  ])

  return Array.from(keys).filter(key => prev[key] !== next[key])
}