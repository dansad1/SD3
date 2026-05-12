import { useEffect, useMemo, useState } from "react"
import { resolvePath } from "@/framework/bind/expression/resolvePath"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"

import type { DataSourceResult } from "../DataSourceResult"

type Params = {
  data?: unknown
}

export function useResourceDataSource<T = unknown>({
  data,
}: Params): DataSourceResult<T> {
  const runtime = usePageRuntimeContext()

  const [remoteData, setRemoteData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)

  /* ================= BIND ($data) ================= */

  const resolvedBind = useMemo(() => {
    if (
      typeof data === "string" &&
      data.startsWith("$")
    ) {
      return resolvePath(
        data.slice(1),
        runtime.data
      )
    }

    return undefined
  }, [data, runtime.data])

  /* ================= RESOURCE FETCH ================= */

 useEffect(() => {
  if (typeof data !== "string") return

  const isResource =
    data.includes(":") || data.startsWith("resource:")

  if (!isResource) return

  const code = data.startsWith("resource:")
    ? data.replace("resource:", "")
    : data

  let cancelled = false

  const load = async () => {
    setLoading(true)

    try {
      const res = await fetch(`/api/resource/${code}/`)
      const json = await res.json()

      if (!cancelled) {
        setRemoteData(json)
      }
    } finally {
      if (!cancelled) {
        setLoading(false)
      }
    }
  }

  load()

  return () => {
    cancelled = true
  }
}, [data])
  /* ================= RESULT ================= */

  if (resolvedBind !== undefined) {
    return {
      data: resolvedBind as T,
      loading: false,
      reload: async () => {},
      meta: {},
    }
  }

  if (remoteData !== null) {
    return {
      data: remoteData,
      loading,
      reload: async () => {},
      meta: {},
    }
  }

  return {
    data: data as T,
    loading,
    reload: async () => {},
    meta: {},
  }
}