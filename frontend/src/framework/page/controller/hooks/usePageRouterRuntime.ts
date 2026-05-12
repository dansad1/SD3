import { useLocation, useParams } from "react-router-dom"
import { useMemo } from "react"

export function usePageRouterRuntime() {
  const params = useParams()
  const location = useLocation()

  const query = useMemo(() => {
    const sp = new URLSearchParams(location.search)

    return Object.fromEntries(sp.entries())
  }, [location.search])

  return {
    params: params as Record<string, string>,
    query,
    location,
  }
}