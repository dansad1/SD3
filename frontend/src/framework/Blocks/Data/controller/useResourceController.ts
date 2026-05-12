import { useEffect } from "react"
import { usePageApi } from "@/framework/page/context/usePageApi"

import type { ResourceBlock } from "../types"
import { resolveResourceParams } from "../runtime/resolveParams"
import { useResourceData } from "../data/useResourceData"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"

export function useResourceController(block: ResourceBlock) {
  const { setDataKey } = usePageApi()
  const runtimeContext = usePageRuntimeContext()

  const params = resolveResourceParams(
    block.params,
    runtimeContext.page.query
  )

  const { data, loading } = useResourceData({
    source: block.source,
    params,
  })

  useEffect(() => {
    if (data !== undefined && block.assign) {
      setDataKey(block.assign, data)
    }
  }, [data, block.assign, setDataKey])

  return { loading }
}