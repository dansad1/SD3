import { useCallback, useState } from "react"

import { unsetDeep } from "./unsetDeep"
import { setDeep } from "./setDeep"

export type PageDataStore = Record<string, unknown>
export type PageRuntimeData = Record<string, unknown>

export function usePageDataStore() {

  const [data, setData] =
    useState<PageDataStore>({})

  const [runtimeData, setRuntimeDataState] =
    useState<PageRuntimeData>({})

  /* ================= SYSTEM DATA ================= */

  const setDataKey = useCallback(
    (
      key: string,
      value: unknown
    ) => {

      setData(prev => {

        const next = { ...prev }

        if (value === undefined) {

          unsetDeep(
            next,
            key
          )

          return next
        }

        setDeep(
          next,
          key,
          value
        )

        return next
      })

    },
    []
  )

  /*
    🔥 ЕДИНЫЙ SCOPE ДЛЯ DSL

    page.getData() теперь видит:
    - data
    - runtimeData

    одинаково как runtimeContext
  */

  const getData = useCallback(
    () => ({

      ...data,

      ...runtimeData,

    }),
    [
      data,
      runtimeData,
    ]
  )

  /* ================= DSL RUNTIME DATA ================= */

  const setRuntimeData = useCallback(
    (
      key: string,
      value: unknown
    ) => {

      setRuntimeDataState(prev => {

        const next = { ...prev }

        if (value === undefined) {

          unsetDeep(
            next,
            key
          )

          return next
        }

        setDeep(
          next,
          key,
          value
        )

        return next
      })

    },
    []
  )

  return {

    data,

    runtimeData,

    setDataKey,

    getData,

    setRuntimeData,
  }
}