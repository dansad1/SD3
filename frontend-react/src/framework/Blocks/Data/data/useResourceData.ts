import { api } from "@/framework/api/client"
import { useEffect, useMemo, useRef, useState } from "react"

type Params = {
  source: string
  params: Record<string, string>
}

export function useResourceData({ source, params }: Params) {
  const [data, setData] = useState<unknown>(null)
  const [loading, setLoading] = useState(false)

  const requestIdRef = useRef(0)

  /* ===============================
     STABLE PARAMS KEY
  =============================== */

  const paramsKey = useMemo(() => {
    return JSON.stringify(params)
  }, [params])

  /* ===============================
     EFFECT
  =============================== */

  useEffect(() => {
  const requestId = ++requestIdRef.current

  const queryParams = new URLSearchParams(params)

  const run = async () => {
    try {
      setLoading(true)

      const res = await api.get(
        `/resource/${source}/?${queryParams.toString()}`
      )

      if (requestId !== requestIdRef.current) return

      setData(res)

    } catch (e) {
      console.error("RESOURCE ERROR:", e)
    } finally {
      if (requestId === requestIdRef.current) {
        setLoading(false)
      }
    }
  }

  run()

  // eslint-disable-next-line react-hooks/exhaustive-deps
}, [source, paramsKey])
  return {
    data,
    loading,
  }
}