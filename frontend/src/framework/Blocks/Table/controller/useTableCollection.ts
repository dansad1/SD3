import { useCallback, useMemo } from "react"

import { traceRuntime } from "@/framework/trace/runtime"
import { api } from "@/framework/api/client"

import { buildQuery } from "@/framework/Blocks/Data/runtime/buildQuery"
import { useAsyncCollection } from "../../hooks/useAsyncCollection"

import type { ApiListResponse } from "../types/api"
import type { BaseRow } from "../types/runtime"

type Options = {
  enabled?: boolean
}

export function useTableCollection<
  T extends BaseRow
>(
  entity: string,
  params: Record<string, unknown>,
  options?: Options,
) {
  const enabled =
    options?.enabled ?? true
  /*
   * QUERY STRING
   */
  const queryString = useMemo(
    () => buildQuery(params),
    [params],
  )
  /*
   * LOAD
   */
  const load = useCallback(
    async (): Promise<ApiListResponse<T>> => {
      if (!enabled ||!entity ||entity === "__disabled__"
      ) {
        return {
          items: [],
          fields: [],
          pagination: {
            page: 1,
            pages: 1,
            total: 0,
            page_size: 25,
          },
          capabilities: {},
        }
      }
      const url =
        `/entity/${entity}/list/?${queryString}`
      const exec = () =>
        api.get<ApiListResponse<T>>(url)
      const trace =
        traceRuntime.current()

      const res = !trace
        ? await exec()
        : await trace.step(
            "table_load",
            exec,
            {
              block: "Table",
              entity,
              query: queryString,
            },
          )

      console.log(
        "API RESPONSE",
        res,
      )
      return res

    },

    [
      entity,
      queryString,
      enabled,
    ],
  )

  /*
   * COLLECTION
   */
  const collection =useAsyncCollection(load)

  /*
   * RESULT
   */

  return {
    items:collection.items ?? [],
    fields:collection.fields ?? [],
    page:collection.page ?? null,
    capabilities:collection.capabilities ?? {},
    loading:collection.loading,
    error:collection.error ?? null,
    reload:collection.reload,

  }
}