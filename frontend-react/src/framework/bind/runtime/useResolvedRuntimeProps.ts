import type { PageRuntimeContext } from "@/framework/bind/types"
import {
  resolveWithContext,
  toPlainSnapshot,
} from "@/framework/bind/runtime/bindRuntime"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import { useMemo } from "react"

export function useResolvedRuntimeProps<
  T extends Record<string, unknown>
>(props: T): T {
  const ctx: PageRuntimeContext = usePageRuntimeContext()

  return useMemo(() => {
    const snapshot = toPlainSnapshot(props)

    return resolveWithContext(snapshot, ctx)
  }, [
    props,
    ctx.data,   // 👈 КРИТИЧНО
    ctx.params,
    ctx.query,
  ])
}