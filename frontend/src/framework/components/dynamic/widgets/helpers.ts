import { resolveWidgetAlias, widgetRegistry } from "../registry"

type MultiValue =
  | string
  | number
  | { value: string | number }

export function normalizeMultiValue(
  v: MultiValue | MultiValue[]
): string[] {
  if (!Array.isArray(v)) return []

  return v.map(item =>
    typeof item === "object"
      ? String(item.value)
      : String(item)
  )
}
export function getWidgetDefinition(
    widget?: string
) {

    const key =
        resolveWidgetAlias(
            widget
        )

    if (!key) {
        return null
    }

    return widgetRegistry[key]

}