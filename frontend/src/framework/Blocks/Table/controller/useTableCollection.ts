import { useCallback, useMemo } from "react"
import { traceRuntime } from "@/framework/trace/runtime"
import { useAsyncCollection } from "../../hooks/useAsyncCollection"

import { buildQuery } from "@/framework/Blocks/Data/runtime/buildQuery"

import type { ApiListResponse } from "../types/api"
import type { BaseRow } from "../types/runtime"
import { api } from "@/framework/api/client"

type Options = {
  enabled?: boolean
}

export function useTableCollection<T extends BaseRow>(
  entity: string,
  params: Record<string, unknown>,
  options?: Options
) {
  const enabled = options?.enabled ?? true

  /* ===============================
     QUERY STRING
  =============================== */

  const queryString = useMemo(() => {
    return buildQuery(params)
  }, [params])

  /* ===============================
     LOAD
  =============================== */

  const load = useCallback(async () => {
    if (!enabled || !entity || entity === "__disabled__") {
      return {
        items: [],
        fields: [],
        page: { page: 1, pages: 1, total: 0 },
        capabilities: {},
      }
    }

    const url = `/entity/${entity}/list/?${queryString}`

    const exec = () => api.get<ApiListResponse<T>>(url)

    const trace = traceRuntime.current()

    const res = !trace
      ? await exec()
      : await trace.step("table_load", exec, {
          block: "Table",
          entity,
          query: queryString,
        })

    return {
      items: res.items ?? res.rows ?? [],
      fields: res.fields ?? [],
      page: res.page,
      capabilities: res.capabilities ?? {},
    }
  }, [entity, queryString, enabled])

  /* ===============================
     COLLECTION
  =============================== */

  const collection = useAsyncCollection(load)

  /* ===============================
     RESULT
  =============================== */

  return {
    items: collection.items ?? [],
    fields: collection.fields ?? [],
    page: collection.page ?? null,
    capabilities: collection.capabilities ?? {},

    loading: collection.loading,
    reload: collection.reload,
  }
}