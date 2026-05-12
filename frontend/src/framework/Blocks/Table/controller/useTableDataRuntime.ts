import { useTableCollection } from "./useTableCollection"
import { useTableDelete } from "./useTableDelete"

import type { BaseRow } from "../types/runtime"
import { useSelection } from "../../hooks/useSelection"

type Options = {
  enabled?: boolean
}

export function useTableDataRuntime<T extends BaseRow>(
  entity: string,
  params: Record<string, unknown>,
  options?: Options
) {
  const enabled = options?.enabled ?? true

  const collection = useTableCollection<T>(
    entity,
    params,   // ✅ теперь правильно
    { enabled }
  )

  const selection = useSelection(collection.items, true)

  const deleteRow = useTableDelete(entity, enabled)

  return {
    fields: collection.fields,
    rows: collection.items,

    loading: enabled ? collection.loading : false,
    page: enabled ? collection.page : null,

    capabilities: collection.capabilities ?? {},

    selection,

    reload: collection.reload,
    delete: deleteRow,
  }
}