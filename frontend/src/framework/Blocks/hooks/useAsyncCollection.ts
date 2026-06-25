import {
  useCallback,
  useEffect,
  useState,
} from "react"

import { parseApiError } from "@/framework/utils/parseApiError"

import type { ApiListResponse } from "../Table/types/api"
import type { BaseRow } from "../Table/types/runtime"


export function useAsyncCollection<
  T extends BaseRow
>(
  loader: () => Promise<ApiListResponse<T>>,
) {

  const [items, setItems] =
    useState<T[]>([])

  const [fields, setFields] =
    useState<
      ApiListResponse<T>["fields"]
    >([])

  const [page, setPage] =
    useState<
      ApiListResponse<T>["pagination"] | null
    >(null)

  const [
    capabilities,
    setCapabilities,
  ] = useState(
    {}
  )

  const [loading, setLoading] =
    useState(false)

  const [error, setError] =
    useState<string | null>(
      null
    )

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
          "PAGINATION:",
          res.pagination
        )

        setItems(

          res.items

          ??

          res.rows

          ??

          []

        )

        setFields(

          res.fields

          ??

          []

        )

        setPage(

          res.pagination

          ??

          null

        )

        setCapabilities(

          res.capabilities

          ??

          {}

        )

      }

      catch (e) {

        const err =
          parseApiError(
            e
          )

        setError(
          err.message
        )

        setItems([])

        setFields([])

        setPage(null)

      }

      finally {

        setLoading(false)

      }

    },

    [

      loader,

    ],

  )


  useEffect(

    () => {

      void load()

    },

    [
      load,
    ],
  )


  return {
    items,
    fields,
    page,
    capabilities,
    loading,
    error,
    reload:
      load,
  }
}