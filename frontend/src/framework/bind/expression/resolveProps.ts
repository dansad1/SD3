// src/framework/bind/expression/resolveProps.ts

import type { BindScope, BindValue } from "../types"
import { resolvePath } from "./resolvePath"
import { evalExpression } from "./evalExpression"

function isBindValue(v: unknown): v is BindValue {
  return (
    typeof v === "object" &&
    v !== null &&
    "bind" in v &&
    typeof (v as Record<string, unknown>).bind === "string"
  )
}

const TOKEN_REGEX = /\$[a-zA-Z0-9_.]+/g
const EXPR_REGEX = /\$\{([^}]+)\}/g

function interpolateString(
  template: string,
  scope: BindScope
): unknown {
  if (!template.includes("$")) return template

  // 🔥 если вся строка = "$path"
  const exactPathMatch = template.match(/^\$([a-zA-Z0-9_.]+)$/)

  if (exactPathMatch) {
    return resolvePath(exactPathMatch[1], scope)
  }

  let unresolved = false

  let result = template.replace(EXPR_REGEX, (_, expr) => {
    const value = evalExpression(expr, scope)

    if (value === undefined) {
      unresolved = true
      return ""
    }

    return String(value)
  })

  result = result.replace(TOKEN_REGEX, (token) => {
    const value = resolvePath(token.slice(1), scope)

    if (value === undefined || value === null) {
      unresolved = true
      return ""
    }

    return String(value)
  })

  if (unresolved) {
    return undefined
  }

  return result
}
function resolveValue(
  value: unknown,
  scope: BindScope
): unknown {
  if (isBindValue(value)) {
    return resolvePath(value.bind, scope)
  }

  if (typeof value === "string") {
    return interpolateString(value, scope)
  }

  if (Array.isArray(value)) {
    return value.map((v) => resolveValue(v, scope))
  }

  if (value && typeof value === "object") {
    const obj = value as Record<string, unknown>
    const out: Record<string, unknown> = {}

    for (const k of Object.keys(obj)) {
      out[k] = resolveValue(obj[k], scope)
    }

    return out
  }

  return value
}

export function resolveProps(
  props: Record<string, unknown>,
  scope: BindScope
): Record<string, unknown> {
  const out: Record<string, unknown> = {}

  for (const key of Object.keys(props)) {
    out[key] = resolveValue(props[key], scope)
  }

  return out
}