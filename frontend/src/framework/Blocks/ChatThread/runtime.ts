// src/framework/Blocks/Chat/runtime.ts

type RuntimeObject = Record<string, unknown>

export function getPathValue(
  source: unknown,
  path: string
): unknown {
  if (!source || typeof source !== "object") {
    return undefined
  }

  const parts = path.split(".").filter(Boolean)

  let current: unknown = source

  for (const part of parts) {
    if (
      current &&
      typeof current === "object" &&
      part in current
    ) {
      current = (current as RuntimeObject)[part]
      continue
    }

    return undefined
  }

  return current
}

export function resolveRuntimeValue(
  value: unknown,
  runtime: unknown
): unknown {
  if (typeof value !== "string") {
    return value
  }

  if (!value.startsWith("$")) {
    return value
  }

  const path = value.slice(1)

  return getPathValue(runtime, path)
}