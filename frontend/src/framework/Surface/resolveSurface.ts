import type { PageChrome } from "@/framework/page/PageSchema"
import type { SurfaceSchema } from "./surface"

export function resolveSurface(
  chrome?: PageChrome
): SurfaceSchema {
  console.log("🧩 resolveSurface input:", chrome)

  const mode =
    chrome?.mode ?? "app"

  const surface: SurfaceSchema = {
    mode,

    areas: {
      topbar:
        chrome?.navbar === false
          ? { type: "empty" }
          : { type: "page" },

      main: {
        type: "page",
      },

      overlay: {
        type: "overlay",
      },

      drawer: {
        type: "drawer",
      },
    },

    options: {
      hideSidebarOnMobile: true,
      lockScrollOnOverlay: true,
    },
  }

  console.log("🧩 resolveSurface output:", surface)

  return surface
}