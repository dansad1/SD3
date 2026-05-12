export function setDeep(
  obj: Record<string, unknown>,
  path: string,
  value: unknown
) {
  const keys = path.split(".")
  let current: any = obj

  keys.forEach((key, index) => {
    if (index === keys.length - 1) {
      current[key] = value
      return
    }

    if (
      typeof current[key] !== "object" ||
      current[key] === null
    ) {
      current[key] = {}
    }

    current = current[key]
  })

  return obj
}