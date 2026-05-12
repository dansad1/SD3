import type { PageEffect, RunEffectsDeps } from "../types"

export function runNavigateEffect(
  effect: Extract<PageEffect, { type: "navigate" }>,
  deps: RunEffectsDeps
) {
  deps.navigate(effect.page)
}