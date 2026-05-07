import type { ApiError } from "@/framework/types/ApiError"
import { parseApiError } from "@/framework/utils/parseApiError"
import { useCallback, useEffect, useState } from "react"

export function useAsyncResource<T>(
  loader: () => Promise<T>,
  options?: { enabled?: boolean }
) {
  const enabled = options?.enabled ?? true

  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<ApiError | null>(null)

  const load = useCallback(async () => {
    if (!enabled) return null

    setLoading(true)
    setError(null)

    try {
      const res = await loader()
      setData(res)
      return res
    } catch (e) {
      const err = parseApiError(e)
      setError(err)
      throw err
    } finally {
      setLoading(false)
    }
  }, [loader, enabled])

  useEffect(() => {
    if (!enabled) return

    ;(async () => {
      await load()
    })()
  }, [load, enabled])

  return {
    data,
    loading,
    error,
    reload: load,
  }
}