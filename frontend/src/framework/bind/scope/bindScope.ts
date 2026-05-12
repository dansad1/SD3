// src/framework/bind/scope/bindScope.ts

import type { BindScope, PageRuntimeContext } from "../types"


function expose(
  scope: Record<string, unknown>,
  obj: Record<string, unknown>
) {
  for (const [k, v] of Object.entries(obj)) {
    scope[k] = v
  }
}

export function buildBindScope(
  ctx: PageRuntimeContext
): BindScope {
  const scope: BindScope = {}

  // =============================
  // CORE
  // =============================

  scope.page = ctx.page

  // 🔥 QUERY
  if (ctx.page?.query) {
    scope.query = ctx.page.query
  } else {
    scope.query = {}
  }

  // 🔥 PARAMS
  if (ctx.page?.params) {
    scope.params = ctx.page.params
  } else {
    scope.params = {}
  }

  // 🔥 USER
  if (ctx.user) {
    scope.user = ctx.user
  }

  if (ctx.me) {
    scope.me = ctx.me
  }

  // 🔥 DATA (самое важное)
  if (ctx.data && typeof ctx.data === "object") {
    scope.data = ctx.data

    // 👇 flat доступ: $pair, $user и т.д.
    expose(scope, ctx.data)
  } else {
    scope.data = {}
  }

  console.log("🔥 BIND SCOPE:", scope)

  return scope
}