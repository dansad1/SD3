import type { DataSourceResult } from "./DataSourceResult"
import { useEntityDataSource } from "./sources/useEntityDataSource"
import { useResourceDataSource } from "./sources/useResourceDataSource"

type Params = {
  entity?: string
  data?: unknown
  params?: Record<string, unknown>
}

export function useDataSource<T = unknown>({
  entity,
  data,
  params,
}: Params): DataSourceResult<T> {

  const resource = useResourceDataSource<T>({
    data,
  })

  const entitySource = useEntityDataSource<T>({
    entity,
    params: params ?? {},
    enabled: data === undefined && !!entity,
  })

  if (data !== undefined) {
    return resource
  }

  if (entity) {
    return entitySource
  }

  return {
    data: [] as T,
    loading: false,
    reload: async () => {},
    meta: {},
  }
}