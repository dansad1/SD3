// src/framework/bind/expression/resolveParams.ts

import { resolveExpression } from "./resolveExpression"


export function resolveParams(
  params: Record<string, unknown> | undefined,
  ctx: Record<string, unknown>
): Record<string, string> {
  const result: Record<string, string> = {}

  if (!params) return result

  for (const [k, v] of Object.entries(params)) {
    const resolved = resolveExpression(v, ctx)

    if (resolved !== undefined && resolved !== null) {
      result[k] = String(resolved)
    }
  }

  return result
}