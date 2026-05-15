// src/framework/Blocks/hooks/useAsyncCollection.ts

import {
  useCallback,
  useEffect,
  useState,
} from "react"

import type {
  BaseRow,
} from "../Table/types/runtime"

import type {
  ApiListResponse,
} from "../Table/types/api"

import {
  parseApiError,
} from "@/framework/utils/parseApiError"

export function useAsyncCollection<
  T extends BaseRow
>(
  loader: () => Promise<ApiListResponse<T>>
) {

  const [items, setItems] =
    useState<T[]>([])

  const [fields, setFields] =
    useState<
      ApiListResponse<T>["fields"]
    >([])

  const [page, setPage] =
    useState<
      ApiListResponse<T>["page"] | null
    >(null)

  const [
    capabilities,
    setCapabilities,
  ] = useState<
    ApiListResponse<T>["capabilities"]
  >({})

  const [loading, setLoading] =
    useState(false)

  const [error, setError] =
    useState<string | null>(null)

  // ============================================
  // LOAD
  // ============================================

  const load = useCallback(
    async () => {

      setLoading(true)

      setError(null)

      try {

        const res =
          await loader()

        console.log(
          "LIST RESPONSE:",
          res
        )

        console.log(
          "LIST FIELDS:",
          res.fields
        )

        setItems(
          res.rows ??
          res.items ??
          []
        )

        setFields(
          res.fields ?? []
        )

        setPage(
          res.page ?? null
        )

        setCapabilities(
          res.capabilities ?? {}
        )

      } catch (e) {

        console.error(
          "TABLE LOAD ERROR",
          e
        )

        const err =
          parseApiError(e)

        setError(
          err.message
        )

        // optional:
        // clear stale data

        setItems([])
        setFields([])

      } finally {

        setLoading(false)
      }
    },
    [loader]
  )

  // ============================================
  // AUTO LOAD
  // ============================================

  useEffect(() => {

    void load()

  }, [load])

  // ============================================
  // RESULT
  // ============================================

  return {

    items,

    fields,

    page,

    capabilities,

    loading,

    error,

    reload: load,
  }
}