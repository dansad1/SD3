import { useMemo } from "react"

import type {
  PageEffect,
  RunEffectsDeps,
} from "./types"

import { runEffect } from "./runEffect"
import { runEffects } from "./runEffects"

type Params = RunEffectsDeps

export function usePageEffectsRuntime(
  deps: Params
) {
  return useMemo(
    () => ({
      runEffect: async (
        effect: PageEffect
      ) => {
        console.log(
          "[usePageEffectsRuntime] runEffect",
          effect
        )

        await runEffect(effect, deps)
      },

      runEffects: async (
        effects?: PageEffect[] | null
      ) => {
        console.log(
          "[usePageEffectsRuntime] runEffects",
          effects
        )

        await runEffects(
          effects ?? [],
          deps
        )
      },
    }),
    [deps]
  )
}