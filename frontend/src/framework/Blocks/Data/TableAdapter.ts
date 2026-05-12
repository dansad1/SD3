import { useMemo, useCallback } from "react"
import { useSelection } from "@/framework/Blocks/hooks/useSelection"
import { useDataSource } from "./useDataSource"

import type {
  BaseRow,
  ListFieldMeta,
  TableCapabilities,
} from "../Table/types/runtime"

import type { TableListData } from "../Table/features/types"

export const noopAsync = async () => {}

/* ========================================================= */

type TableBlockLike = {
  entity?: string
  data?: unknown
}

type ResourceLike = {
  rows?: unknown[]
  items?: unknown[]
  fields?: unknown[]
  page?: unknown
  capabilities?: unknown
}

/* ========================================================= */

function isObject(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null
}

function isResourceLike(v: unknown): v is ResourceLike {
  return isObject(v)
}

/* ========================================================= */

export function useTableData<T extends BaseRow>(
  block: TableBlockLike,
  params: Record<string, unknown>
): TableListData<T> {
  const ds = useDataSource({
    entity: block.entity,
    data: block.data,
    params,
  })

  /* ================= ROWS ================= */

  const rows = useMemo<T[]>(() => {
    const raw = ds.data

    if (Array.isArray(raw)) {
      return raw as T[]
    }

    if (isResourceLike(raw)) {
      if (Array.isArray(raw.rows)) {
        return raw.rows as T[]
      }

      if (Array.isArray(raw.items)) {
        return raw.items as T[]
      }
    }

    return []
  }, [ds.data])

  /* ================= FIELDS ================= */

  const fields = useMemo<ListFieldMeta[]>(() => {
    const raw = ds.data

    if (isResourceLike(raw) && Array.isArray(raw.fields)) {
      return raw.fields as ListFieldMeta[]
    }

    const sourceRows: unknown[] =
      Array.isArray(raw)
        ? raw
        : isResourceLike(raw) && Array.isArray(raw.rows)
          ? raw.rows
          : isResourceLike(raw) && Array.isArray(raw.items)
            ? raw.items
            : []

    const firstRow = sourceRows[0]

    if (
      firstRow &&
      typeof firstRow === "object" &&
      !Array.isArray(firstRow)
    ) {
      return Object.keys(firstRow)
        .filter(key => !key.endsWith("_id"))
        .map(key => ({
          key,
          label: key
            .replace(/_/g, " ")
            .replace(/\b\w/g, s => s.toUpperCase()),
          sortable: false,
        }))
    }

    return []
  }, [ds.data])

  /* ================= PAGE ================= */

  const page = useMemo<TableListData<T>["page"]>(() => {
    const raw = ds.data

    if (isResourceLike(raw) && raw.page && isObject(raw.page)) {
      return raw.page as TableListData<T>["page"]
    }

    return ds.meta?.page ?? null
  }, [ds.data, ds.meta])

  /* ================= CAPABILITIES ================= */

  const capabilities = useMemo<TableCapabilities>(() => {
    const raw = ds.data

    if (isResourceLike(raw) && isObject(raw.capabilities)) {
      return raw.capabilities as TableCapabilities
    }

    return (ds.meta?.capabilities as TableCapabilities) ?? {}
  }, [ds.data, ds.meta])

  /* ================= SELECTION ================= */

  const selection = useSelection(rows, true)

  /* ================= DELETE ================= */

  const deleteRow = useCallback(
    async (id: string | number): Promise<boolean> => {
      void id
      return false
    },
    []
  )

  /* ================= RESULT ================= */

  return {
    fields,
    rows,
    loading: ds.loading,
    page,
    capabilities,
    selection,
    reload: ds.reload ?? noopAsync,
    delete: deleteRow,
  }
}