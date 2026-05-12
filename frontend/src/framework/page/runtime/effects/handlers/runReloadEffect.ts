import type { PageEffect, RunEffectsDeps } from "../types"

export function runReloadEffect(
  effect: Extract<PageEffect, { type: "reload" }>,
  deps: RunEffectsDeps
) {
  deps.emit(`reload:${effect.target}`)
}