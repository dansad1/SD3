import type { PageEffect, RunEffectsDeps } from "../types"

export function runEmitEffect(
  effect: Extract<PageEffect, { type: "emit" }>,
  deps: RunEffectsDeps
) {
  deps.emit(effect.event, effect.payload)
}