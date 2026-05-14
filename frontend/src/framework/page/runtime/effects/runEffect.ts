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
    case "toast":
      return await runToastEffect(effect, deps)

    case "navigate":
      return await runNavigateEffect(effect, deps)

    case "reload":
      return await runReloadEffect(effect, deps)

    case "set_data":
      return await runSetDataEffect(effect, deps)

    case "emit":
      return await runEmitEffect(effect, deps)

    case "close_modal":
      return await runCloseModalEffect(effect, deps)

    case "open_modal":
      return await runOpenModalEffect(effect, deps)

    case "auth.reload_user": {
      console.log("[runEffect] auth.reload_user")

      const refresh = (window as any).__refreshAuth

      if (typeof refresh === "function") {
        await refresh()
      }

      return
    }

    default: {
      const exhaustive: never = effect

      console.warn(
        "[effects] unknown effect",
        exhaustive
      )
    }
  }
}