import type {
  SurfaceDrawerState,
  SurfaceSchema,
} from "../surface"

export function createDrawerModule(
  update: (fn: (s: SurfaceSchema) => void) => boolean,
  emit: () => void
) {
  return {
    setDrawer(value: Partial<SurfaceDrawerState>) {
      const ok = update(s => {
        s.drawer = {
          open: false,
          side: "right",
          ...s.drawer,
          ...value,
        }
      })
      if (ok) emit()
    },

    openDrawer(
      component: string,
      payload?: Record<string, unknown>,
      side: "left" | "right" | "bottom" = "right"
    ) {
      const ok = update(s => {
        s.drawer = {
          open: true,
          component,
          payload,
          side,
        }
      })
      if (ok) emit()
    },

    closeDrawer() {
      const ok = update(s => {
        s.drawer = { open: false }
      })
      if (ok) emit()
    },

    clearDrawer() {
      const ok = update(s => {
        s.drawer = undefined
      })
      if (ok) emit()
    },
  }
}