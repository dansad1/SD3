import type { SurfaceSchema } from "../surface"

export function createOptionsModule(
  update: (fn: (s: SurfaceSchema) => void) => boolean,
  emit: () => void
) {
  return {
    setOptions(
      value: Partial<
        NonNullable<SurfaceSchema["options"]>
      >
    ) {
      const ok = update(s => {
        s.options = {
          ...s.options,
          ...value,
        }
      })
      if (ok) emit()
    },
  }
}