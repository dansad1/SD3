export function unsetDeep(
  obj: Record<string, unknown>,
  path: string
) {
  const keys = path.split(".")
  let current: any = obj

  keys.forEach((key, index) => {
    if (!current) return

    if (index === keys.length - 1) {
      delete current[key]
      return
    }

    current = current[key]
  })

  return obj
}