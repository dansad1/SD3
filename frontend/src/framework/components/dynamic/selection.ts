function normalize(v: unknown) {
  return String(v)
}

export function isSelected(
  selected: unknown,
  value: string | number,
  multiple?: boolean
) {
  if (multiple) {
    if (!Array.isArray(selected)) return false

    return selected
      .map(normalize)
      .includes(normalize(value))
  }

  return normalize(selected) === normalize(value)
}

export function toggleValue(
  selected: unknown,
  value: string | number,
  multiple?: boolean
) {
  if (multiple) {
    const list = Array.isArray(selected) ? selected : []

    const exists = list
      .map(normalize)
      .includes(normalize(value))

    if (exists) {
      return list.filter(
        v => normalize(v) !== normalize(value)
      )
    }

    return [...list, value]
  }

  return value
}