import { useSearchParams } from "react-router-dom"

export function useTableQueryRuntime() {
  const [params, setParams] = useSearchParams()

  const page = Number(params.get("page") ?? 1)
  const sort = params.get("sort") ?? undefined
  const search = params.get("q") ?? ""

  const updateParams = (updater: (p: URLSearchParams) => void) => {
    const next = new URLSearchParams(params)
    updater(next)
    setParams(next)
  }

  const setPage = (p: number) => {
    updateParams(next => {
      next.set("page", String(p))
    })
  }

  const setSort = (s: string) => {
    updateParams(next => {
      next.set("sort", s)
      next.set("page", "1")
    })
  }

  const setSearch = (q: string) => {
    updateParams(next => {
      if (q) next.set("q", q)
      else next.delete("q")

      next.set("page", "1")
    })
  }

  return {
    page,
    sort,
    search,
    params,
    setPage,
    setSort,
    setSearch,
  }
}