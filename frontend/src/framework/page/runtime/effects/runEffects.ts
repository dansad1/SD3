import type {
  PageEffect,
  RunEffectsDeps,
} from "./types"

import { runEffect } from "./runEffect"

export async function runEffects(
  effects: PageEffect[] | null | undefined,
  deps: RunEffectsDeps
): Promise<void> {
  const normalized = effects ?? []

  console.log("[runEffects] start", normalized)

  for (const effect of normalized) {
    console.log("[runEffects] effect", effect)

    await runEffect(effect, deps)
  }

  console.log("[runEffects] done")
}