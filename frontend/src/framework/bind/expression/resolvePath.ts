// src/framework/bind/expression/resolvePath.ts

export function resolvePath(
  path: string,
  ctx: unknown
): unknown {
  if (!path) return undefined

  const parts = path.split(".").filter(Boolean)
  let cur: unknown = ctx

  for (const key of parts) {
    if (cur === null || cur === undefined) return undefined
    if (typeof cur !== "object") return undefined

    const rec = cur as Record<string, unknown>
    cur = rec[key]
  }

  return cur
}