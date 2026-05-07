import { useTableCollection } from "@/framework/Blocks/Table/controller/useTableCollection"
import type { DataSourceResult } from "../DataSourceResult"

type Params = {
  entity?: string
  params: Record<string, unknown>
  enabled: boolean
}

export function useEntityDataSource<T>({
  entity,
  params,
  enabled,
}: Params): DataSourceResult<T> {

  const list = useTableCollection(
    entity ?? "__disabled__",
    params,
    { enabled }
  )

  return {
    data: {
      items: list.items,
      fields: list.fields,
    } as unknown as T,

    loading: list.loading,
    reload: list.reload,

    meta: {
      page: list.page ?? undefined,
      capabilities: list.capabilities,
    },
  }
}