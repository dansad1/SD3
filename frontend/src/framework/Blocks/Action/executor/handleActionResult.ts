import type { PageApi } from "@/framework/page/context/types"
import { isActionResult } from "./isActionResult"

export function handleActionResult(
  page: PageApi,
  result: unknown
) {
  if (!isActionResult(result)) {
    return
  }

  if (
    Array.isArray(result.effects) &&
    result.effects.length > 0
  ) {
    page.runEffects(result.effects)
  }

  if (result.redirect) {
    page.runEffect({
      type: "navigate",
      page: result.redirect,
    })
  }

  if (result.message) {
    page.runEffect({
      type: "toast",
      variant:
        result.status === "error"
          ? "error"
          : "success",
      message: result.message,
    })
  }
}