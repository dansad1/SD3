// table/runtime/executable/interpolateTarget.ts

import { getByPath } from "./getByPath"

export function interpolateTarget(
  target: string,
  ctx: Record<string, unknown>
) {
  const row =
    ctx.row &&
    typeof ctx.row === "object"
      ? (ctx.row as Record<string, unknown>)
      : undefined

  if (target.startsWith("$row.")) {
    if (!row) {
      return undefined
    }

    const path = target.replace("$row.", "")
    const value = getByPath(row, path)

    return typeof value === "string"
      ? value
      : undefined
  }

  let resolved = target

  if (row) {
    const matches = resolved.match(
      /\$row\.[a-zA-Z0-9_.]+/g
    )

    if (matches) {
      for (const match of matches) {
        const path = match.replace(
          "$row.",
          ""
        )

        const value = getByPath(row, path)

        if (
          value === null ||
          value === undefined
        ) {
          continue
        }

        resolved = resolved.replaceAll(
          match,
          String(value)
        )
      }
    }
  }

  for (const key in ctx) {
    const value = ctx[key]

    if (
      value === null ||
      value === undefined
    ) {
      continue
    }

    resolved = resolved.replaceAll(
      `$${key}`,
      String(value)
    )
  }

  return resolved
}