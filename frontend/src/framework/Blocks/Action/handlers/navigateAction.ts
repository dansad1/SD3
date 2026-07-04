// src/framework/Blocks/Action/actions/navigate.ts

import type { ActionContext } from "../types"

export async function navigateAction(
  to: string,
  ctx: ActionContext = {},
): Promise<boolean> {

  if (!to) {

    console.warn(
      "navigateAction: empty target",
    )

    return false

  }

  const params = new URLSearchParams()

  /* =========================
     1. CURRENT QUERY
  ========================= */

  if (ctx.page?.query) {

    for (const [key, value] of Object.entries(
      ctx.page.query,
    )) {

      if (value != null) {

        params.set(
          key,
          String(value),
        )

      }

    }

  }

  /* =========================
     2. PAGE PARAMS
  ========================= */

  if (ctx.page?.params) {

    for (const [key, value] of Object.entries(
      ctx.page.params,
    )) {

      if (value != null) {

        params.set(
          key,
          String(value),
        )

      }

    }

  }

  /* =========================
     3. ACTION CONTEXT
  ========================= */

  for (const [key, value] of Object.entries(
    ctx,
  )) {

    if (

      key === "page"

      ||

      value == null

    ) {

      continue

    }

    params.set(

      key,

      String(value),

    )

  }

  /* =========================
     BUILD URL
  ========================= */

  const query = params.toString()

  const url = to.startsWith("/")

    ? (

      query

        ? `${to}?${query}`

        : to

    )

    : (

      query

        ? `/page/${to}?${query}`

        : `/page/${to}`

    )

  /* =========================
     NAVIGATE
  ========================= */

  window.history.pushState(
    {},
    "",
    url,
  )

  window.dispatchEvent(
    new PopStateEvent(
      "popstate",
    ),
  )

  return true

}