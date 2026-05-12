export function buildQuery(
  params: Record<string, unknown>
): string {
  const query = new URLSearchParams()

  for (const key in params) {
    const value = params[key]

    if (
      value === undefined ||
      value === null ||
      value === "" ||
      value === "undefined"
    ) {
      continue
    }

    query.set(key, String(value))
  }

  return query.toString()
}