// src/framework/bind/expression/resolveExpression.ts

export function resolveExpression(
  expr: unknown,
  data: Record<string, unknown>
): unknown {
  console.log("---- resolveExpression ----")
  console.log("expr:", expr)
  console.log("ctx:", data)

  if (typeof expr !== "string") {
    console.log("not a string → return as is")
    return expr
  }

  if (!expr.startsWith("$")) {
    console.log("not a DSL expr → return as is")
    return expr
  }

  // =========================
  // MATH EXPRESSION
  // =========================
  if (expr.includes("+") || expr.includes("-")) {
    try {
      const replaced = expr.replace(/\$[a-zA-Z0-9_.]+/g, (match) => {
        console.log("match:", match)

        const path = match.slice(1).split(".")
        let cur: unknown = data

        for (const p of path) {
          console.log("  step:", p, "cur:", cur)

          if (
            typeof cur !== "object" ||
            cur === null ||
            !(p in (cur as Record<string, unknown>))
          ) {
            console.log("  ❌ path not found → 0")
            return "0"
          }

          cur = (cur as Record<string, unknown>)[p]
        }

        console.log("  ✅ resolved:", cur)
        return String(cur ?? 0)
      })

      console.log("expression replaced:", replaced)

      const result = Function(`"use strict"; return (${replaced})`)()
      console.log("result:", result)

      return result
    } catch (e) {
      console.error("resolveExpression error:", expr, e)
      return undefined
    }
  }

  // =========================
  // SIMPLE PATH
  // =========================
  const path = expr.slice(1).split(".")
  let cur: unknown = data

  for (const p of path) {
    console.log("path step:", p, "cur:", cur)

    if (
      typeof cur !== "object" ||
      cur === null ||
      !(p in (cur as Record<string, unknown>))
    ) {
      console.log("❌ path not found:", p)
      return undefined
    }

    cur = (cur as Record<string, unknown>)[p]
  }

  console.log("✅ FINAL VALUE:", cur)
  return cur
}