import type {
  SurfaceArea,
  SurfaceContent,
  SurfaceSchema,
} from "../surface"

export function createAreaModule(
  update: (fn: (s: SurfaceSchema) => void) => boolean,
  emit: () => void
) {
  return {
    setArea(area: SurfaceArea, content?: SurfaceContent) {
      const ok = update(s => {
        if (content) {
          s.areas[area] = content
        } else {
          delete s.areas[area]
        }
      })
      if (ok) emit()
    },

    clearArea(area: SurfaceArea) {
      const ok = update(s => {
        delete s.areas[area]
      })
      if (ok) emit()
    },

    clearAreas() {
      const ok = update(s => {
        s.areas = {}
      })
      if (ok) emit()
    },
  }
}