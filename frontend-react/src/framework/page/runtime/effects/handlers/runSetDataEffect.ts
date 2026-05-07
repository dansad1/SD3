import type { PageEffect, RunEffectsDeps } from "../types"

export function runSetDataEffect(
  effect: Extract<PageEffect, { type: "set_data" }>,
  deps: RunEffectsDeps
) {
  deps.setDataKey(effect.key, effect.value)
}