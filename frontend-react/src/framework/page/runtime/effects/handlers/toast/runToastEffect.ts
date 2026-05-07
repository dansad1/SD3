import type { PageEffect, RunEffectsDeps, EffectToastVariant } from "../types"

function defaultToast(
  message: string,
  variant: EffectToastVariant = "info"
) {
  console.log(`[toast:${variant}] ${message}`)
}

export function runToastEffect(
  effect: Extract<PageEffect, { type: "toast" }>,
  deps: RunEffectsDeps
) {
  const toast = deps.toast ?? defaultToast
  toast(effect.message, effect.variant)
}