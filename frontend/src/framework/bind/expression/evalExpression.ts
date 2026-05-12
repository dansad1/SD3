// src/framework/bind/expression/evalExpression.ts

import { resolvePath } from "./resolvePath"
import type { BindScope } from "../types"

const TOKEN_REGEX = /\$[a-zA-Z0-9_.]+/g

function replaceTokens(expr: string, scope: BindScope): string {
  return expr.replace(TOKEN_REGEX, (token) => {
    const value = resolvePath(token.slice(1), scope)
    return JSON.stringify(value ?? null)
  })
}

export function evalExpression(
  expr: string,
  scope: BindScope
): unknown {
  const replaced = replaceTokens(expr, scope)

  try {
    return Function(`"use strict"; return (${replaced})`)()
  } catch (e) {
    console.warn("Expression error:", expr, e)
    return undefined
  }
}