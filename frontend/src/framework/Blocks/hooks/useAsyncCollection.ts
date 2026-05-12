import { useCallback, useEffect, useState } from "react"
import type { BaseRow } from "../Table/types/runtime"
import type { ApiListResponse } from "../Table/types/api"

export function useAsyncCollection<T extends BaseRow>(
  loader: () => Promise<ApiListResponse<T>>
) {
  const [items, setItems] = useState<T[]>([])
  const [fields, setFields] =
    useState<ApiListResponse<T>["fields"]>([])
  const [page, setPage] =
    useState<ApiListResponse<T>["page"] | null>(null)
  const [capabilities, setCapabilities] =
    useState<ApiListResponse<T>["capabilities"]>({})
  const [loading, setLoading] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)

    try {
      const res = await loader()

      console.log("LIST RESPONSE:", res)
      console.log("LIST FIELDS:", res.fields)

      setItems(res.rows ?? res.items ?? [])
      setFields(res.fields ?? [])
      setPage(res.page ?? null)
      setCapabilities(res.capabilities ?? {})
    } finally {
      setLoading(false)
    }
  }, [loader])

  useEffect(() => {
    load()
  }, [load])

  return {
    items,
    fields,
    page,
    capabilities,
    loading,
    reload: load,
  }
}