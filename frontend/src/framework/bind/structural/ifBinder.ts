// src/framework/bind/structural/ifBinder.ts

import { registerStructuralBinder } from "./registry"
import { resolvePath } from "../expression/resolvePath"
import { evalExpression } from "../expression/evalExpression"
import type { BindScope, AnyBlock, BindResult } from "../types"

/* =========================================================
   CONDITION RESOLVER
========================================================= */

function resolveCondition(
  when: unknown,
  scope: BindScope
): boolean {
  // boolean напрямую
  if (typeof when === "boolean") {
    return when
  }

  // не строка → false
  if (typeof when !== "string") {
    return false
  }

  const expr = when.trim()

  if (!expr) return false

  // literal
  if (expr === "true") return true
  if (expr === "false") return false

  /* =========================
     ${ expression }
  ========================= */

  if (expr.startsWith("${") && expr.endsWith("}")) {
    return !!evalExpression(expr.slice(2, -1), scope)
  }

  /* =========================
     !$path
  ========================= */

  if (expr.startsWith("!$")) {
    return !resolvePath(expr.slice(2), scope)
  }

  /* =========================
     $path
  ========================= */

  if (expr.startsWith("$")) {
    return !!resolvePath(expr.slice(1), scope)
  }

  /* =========================
     fallback
  ========================= */

  return !!expr
}

/* =========================================================
   BINDER
========================================================= */

registerStructuralBinder({
  type: "if",

  bind(block: AnyBlock, scope: BindScope, bindChild): BindResult {
    const ok = resolveCondition(block.when, scope)

    if (!ok) {
      return null
    }

    const children = Array.isArray(block.blocks)
      ? (block.blocks as AnyBlock[])
      : []

    const out: AnyBlock[] = []

    for (const child of children) {
      const bound = bindChild(child, scope)

      if (Array.isArray(bound)) {
        out.push(...bound)
      } else if (bound) {
        out.push(bound)
      }
    }

    return out
  },
})