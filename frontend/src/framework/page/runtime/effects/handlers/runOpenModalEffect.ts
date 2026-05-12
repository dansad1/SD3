import type { PageEffect, RunEffectsDeps } from "../types"

export function runOpenModalEffect(
  effect: Extract<PageEffect, { type: "open_modal" }>,
  deps: RunEffectsDeps
) {
  deps.emit("modal:open", {
    modal: effect.modal,
    payload: effect.payload,
  })
}