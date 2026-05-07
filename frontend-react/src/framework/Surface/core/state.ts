import type { SurfaceSchema } from "../surface"

export function createSurfaceState(
  surface: SurfaceSchema | null
) {
  let state = surface

  return {
    get() {
      return state
    },
    set(next: SurfaceSchema | null) {
      state = next
    },
    update(fn: (s: SurfaceSchema) => void) {
      if (!state) return false
      fn(state)
      return true
    },
  }
}