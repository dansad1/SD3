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

  console.group("[IF] resolveCondition")
  console.log("when =", when)
  console.log("scope =", scope)

  // boolean напрямую
  if (typeof when === "boolean") {
    console.log("boolean =>", when)
    console.groupEnd()
    return when
  }

  // не строка → false
  if (typeof when !== "string") {
    console.log("not string => false")
    console.groupEnd()
    return false
  }

  const expr = when.trim()

  if (!expr) {
    console.log("empty => false")
    console.groupEnd()
    return false
  }

  // literal
  if (expr === "true") {
    console.log("literal true")
    console.groupEnd()
    return true
  }

  if (expr === "false") {
    console.log("literal false")
    console.groupEnd()
    return false
  }

  /* =========================
     ${ expression }
  ========================= */

  if (expr.startsWith("${") && expr.endsWith("}")) {

    const value =
      evalExpression(
        expr.slice(2, -1),
        scope
      )

    console.log(
      "expression",
      expr,
      "=>",
      value
    )

    console.groupEnd()

    return !!value
  }

  /* =========================
     !$path
  ========================= */

  if (expr.startsWith("!$")) {

    const value =
      resolvePath(
        expr.slice(2),
        scope
      )

    console.log(
      "negated path",
      expr,
      "=>",
      value
    )

    console.groupEnd()

    return !value
  }

  /* =========================
     $path
  ========================= */

  if (expr.startsWith("$")) {

    const value =
      resolvePath(
        expr.slice(1),
        scope
      )

    console.log(
      "path",
      expr,
      "=>",
      value
    )

    console.groupEnd()

    return !!value
  }

  /* =========================
     fallback
  ========================= */

  console.log(
    "fallback =>",
    !!expr
  )

  console.groupEnd()

  return !!expr
}

/* =========================================================
   BINDER
========================================================= */

registerStructuralBinder({
  type: "if",

  bind(
    block: AnyBlock,
    scope: BindScope,
    bindChild
  ): BindResult {

    console.group("[IF] bind")
    console.log("block =", block)
    console.log("scope =", scope)

    const ok =
      resolveCondition(
        block.when,
        scope
      )

    console.log("result =", ok)

    console.groupEnd()

    if (!ok) {
      return null
    }

    const children = Array.isArray(block.blocks)
      ? (block.blocks as AnyBlock[])
      : []

    const out: AnyBlock[] = []

    for (const child of children) {

      const bound =
        bindChild(child, scope)

      if (Array.isArray(bound)) {
        out.push(...bound)
      } else if (bound) {
        out.push(bound)
      }
    }

    return out
  },
})