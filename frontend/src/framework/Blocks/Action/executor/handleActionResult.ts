import type { PageApi }
  from "@/framework/page/context/types"

import { isActionResult }
  from "./isActionResult"

export function handleActionResult(
  page: PageApi,
  result: unknown
) {

  if (!isActionResult(result)) {
    return
  }

  /* ========================================
     EFFECTS
  ======================================== */

  if (
    Array.isArray(result.effects) &&
    result.effects.length > 0
  ) {
    page.runEffects(result.effects)
  }

  /* ========================================
     REDIRECT
  ======================================== */

  if (result.redirect) {

    page.runEffect({
      type: "navigate",
      page: result.redirect,
    })
  }

  /* ========================================
     MESSAGE
  ======================================== */

  let message = result.message

  /* ========================================
     VALIDATION ERRORS
  ======================================== */

  if (
    !message &&
    result.status === "error" &&
    result.errors
  ) {

    const firstError =
      Object
        .values(result.errors)
        ?.flat?.()?.[0]

    if (typeof firstError === "string") {
      message = firstError
    }
  }

  /* ========================================
     TOAST
  ======================================== */

  if (message) {

    page.runEffect({
      type: "toast",

      variant:
        result.status === "error"
          ? "error"
          : "success",

      message,
    })
  }
}