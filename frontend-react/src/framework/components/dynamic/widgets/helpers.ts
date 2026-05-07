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
