// src/framework/bind/processors/sugarDollar.ts


import { resolvePath } from "../expression/resolvePath"
import { registerBindProcessor } from "./bindRegistry"
import type { BindScope } from "../types"

function resolveDollar(v: unknown, scope: BindScope): unknown {
  if (typeof v === "string" && v.startsWith("$")) {
    return resolvePath(v.slice(1), scope)
  }
  return v
}

/**
 * Позволяет писать в DSL:
 *   value="$role.name"
 * вместо:
 *   value={{ bind: "role.name" }}
 */
registerBindProcessor((block, scope) => {
  // рекурсивно не делаем: resolveProps уже рекурсивный.
  // здесь только сахар для строк верхнего уровня props.
  const out: Record<string, unknown> = {}

  for (const [k, v] of Object.entries(block)) {
    out[k] = resolveDollar(v, scope)
  }

  return out
})