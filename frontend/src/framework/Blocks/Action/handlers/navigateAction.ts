// src/framework/Blocks/Action/actions/navigate.ts

import type { ActionContext } from "../types"

export async function navigateAction(
  to: string,
  ctx: ActionContext = {}
): Promise<boolean> {
    console.log("NAVIGATE CTX:", ctx) // 👈 ВАЖНО

  if (!to) {
    console.warn("navigateAction: empty target")
    return false
  }

  const params = new URLSearchParams()

  /* =========================
     1. CURRENT QUERY
  ========================= */
  if (ctx.page?.query) {
    for (const [k, v] of Object.entries(ctx.page.query)) {
      if (v != null) {
        params.set(k, String(v))
      }
    }
  }

  /* =========================
     2. PAGE PARAMS
  ========================= */
  if (ctx.page?.params) {
    for (const [k, v] of Object.entries(ctx.page.params)) {
      if (v != null) {
        params.set(k, String(v))
      }
    }
  }

  /* =========================
     3. ENTITY CONTEXT (🔥 FIX)
  ========================= */
  if (ctx.id != null) {
    params.set("id", String(ctx.id))
  }

  /* =========================
     BUILD URL
  ========================= */
  const query = params.toString()

  const url = to.startsWith("/")
    ? (query ? `${to}?${query}` : to)
    : (query ? `/page/${to}?${query}` : `/page/${to}`)

  /* =========================
     NAVIGATE
  ========================= */
  window.history.pushState({}, "", url)
  window.dispatchEvent(new PopStateEvent("popstate"))

  return true
}