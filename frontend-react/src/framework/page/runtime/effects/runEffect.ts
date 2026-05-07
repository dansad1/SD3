import type {
  PageEffect,
  RunEffectsDeps,
} from "./types"

import { runNavigateEffect } from "./handlers/runNavigateEffect"
import { runReloadEffect } from "./handlers/runReloadEffect"
import { runSetDataEffect } from "./handlers/runSetDataEffect"
import { runEmitEffect } from "./handlers/runEmitEffect"
import { runCloseModalEffect } from "./handlers/runCloseModalEffect"
import { runOpenModalEffect } from "./handlers/runOpenModalEffect"
import { runToastEffect } from "./handlers/toast/runToastEffect"

export async function runEffect(
  effect: PageEffect,
  deps: RunEffectsDeps
): Promise<void> {
  console.log("[runEffect] incoming", effect)

  switch (effect.type) {
    case "toast": {
      console.log("[runEffect] toast", {
        message: effect.message,
        variant: effect.variant,
      })

      return await runToastEffect(effect, deps)
    }

    case "navigate": {
      console.log("[runEffect] navigate", {
        page: effect.page,
      })

      return await runNavigateEffect(effect, deps)
    }

    case "reload": {
      console.log("[runEffect] reload", {
        target: effect.target,
      })

      return await runReloadEffect(effect, deps)
    }

    case "set_data": {
      console.log("[runEffect] set_data", {
        key: effect.key,
        value: effect.value,
      })

      return await runSetDataEffect(effect, deps)
    }

    case "emit": {
      console.log("[runEffect] emit", {
        event: effect.event,
        payload: effect.payload,
      })

      return await runEmitEffect(effect, deps)
    }

    case "close_modal": {
      console.log("[runEffect] close_modal")

      return await runCloseModalEffect(effect, deps)
    }

    case "open_modal": {
      console.log("[runEffect] open_modal", {
        modal: effect.modal,
        payload: effect.payload,
      })

      return await runOpenModalEffect(effect, deps)
    }

    /* ================= AUTH ================= */

    case "auth.reload_user": {
      console.log("[runEffect] auth.reload_user")

      window.dispatchEvent(
        new CustomEvent("app:effect", {
          detail: { type: "auth.reload_user" },
        })
      )

      return
    }

    /* ================= FALLBACK ================= */

    default: {
      const exhaustive: never = effect

      console.warn(
        "[effects] unknown effect",
        exhaustive
      )
    }
  }
}