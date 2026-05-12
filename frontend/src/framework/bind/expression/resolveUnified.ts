type Ctx = Record<string, any>

function resolvePath(path: string, ctx: Ctx): any {
  const parts = path.split(".")
  let cur = ctx

  for (const p of parts) {
    if (cur == null) return undefined
    cur = cur[p]
  }

  return cur
}

export function resolveValue(value: any, ctx: Ctx): any {
  if (typeof value !== "string") return value

  if (!value.startsWith("$")) return value

  // $query.id → query.id
  const path = value.slice(1)

  return resolvePath(path, ctx)
}

export function resolveObject(obj: any, ctx: Ctx): any {
  if (Array.isArray(obj)) {
    return obj.map(v => resolveObject(v, ctx))
  }

  if (obj && typeof obj === "object") {
    const result: Record<string, any> = {}

    for (const key in obj) {
      result[key] = resolveObject(obj[key], ctx)
    }

    return result
  }

  return resolveValue(obj, ctx)
}