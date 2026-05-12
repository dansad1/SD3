import type {
  SurfaceTopbarState,
  SurfaceSchema,
} from "../surface"

export function createTopbarModule(
  update: (fn: (s: SurfaceSchema) => void) => boolean,
  emit: () => void
) {
  return {
    setTopbar(value: Partial<SurfaceTopbarState>) {
      const ok = update(s => {
        s.topbar = {
          ...s.topbar,
          ...value,
        }
      })
      if (ok) emit()
    },

    clearTopbar() {
      const ok = update(s => {
        s.topbar = undefined
      })
      if (ok) emit()
    },
  }
}