import type {
  SurfaceOverlayState,
  SurfaceSchema,
} from "../surface"

export function createOverlayModule(
  update: (fn: (s: SurfaceSchema) => void) => boolean,
  emit: () => void
) {
  return {
    setOverlay(value: Partial<SurfaceOverlayState>) {
      const ok = update(s => {
        s.overlay = {
          open: false,
          ...s.overlay,
          ...value,
        }
      })
      if (ok) emit()
    },

    openOverlay(
      component: string,
      payload?: Record<string, unknown>
    ) {
      const ok = update(s => {
        s.overlay = {
          open: true,
          component,
          payload,
        }
      })
      if (ok) emit()
    },

    closeOverlay() {
      const ok = update(s => {
        s.overlay = { open: false }
      })
      if (ok) emit()
    },

    clearOverlay() {
      const ok = update(s => {
        s.overlay = undefined
      })
      if (ok) emit()
    },
  }
}