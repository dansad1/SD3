import { useMemo } from "react"

export function useTableQueryString(
  params: Record<string, unknown>
) {
  return useMemo(() => {
    const query = new URLSearchParams()

    for (const key in params) {
      const value = params[key]
      if (value === undefined || value === null) continue

      query.set(key, String(value))
    }

    return query.toString()
  }, [params])
}