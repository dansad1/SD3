import type { SurfaceSchema } from "./surface";

export const appSurface: SurfaceSchema = {
  mode: "app",

  areas: {
    main: { type: "page" },
  },

  options: {
    hideSidebarOnMobile: true,
  },
}
