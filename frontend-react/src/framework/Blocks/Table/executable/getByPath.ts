// table/runtime/executable/getByPath.ts

export function getByPath(
  obj: Record<string, unknown>,
  path: string
): unknown {
  return path
    .split(".")
    .reduce<unknown>((acc, key) => {
      if (
        acc &&
        typeof acc === "object"
      ) {
        return (acc as Record<string, unknown>)[key]
      }

      return undefined
    }, obj)
}