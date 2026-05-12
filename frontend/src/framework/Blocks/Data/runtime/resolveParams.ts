export function resolveResourceParams(
  params: Record<string, unknown> | undefined,
  query: Record<string, string>
) {
  const result: Record<string, string> = {}

  if (!params) return result

  for (const [key, value] of Object.entries(params)) {
    if (typeof value === "string" && value.startsWith("$query.")) {
      const k = value.replace("$query.", "")
      const v = query[k]

      if (v != null && v !== "") {
        result[key] = String(v)
      }
      continue
    }

    if (
      value !== undefined &&
      value !== null &&
      value !== "" &&
      value !== "undefined"
    ) {
      result[key] = String(value)
    }
  }

  return result
}