import type { PageEffect, RunEffectsDeps } from "../types"

export function runCloseModalEffect(
  _effect: Extract<PageEffect, { type: "close_modal" }>,
  deps: RunEffectsDeps
) {
  deps.emit("modal:close")
}