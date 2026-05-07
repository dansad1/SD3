import { useEffect } from "react"
import { traceRuntime } from "@/framework/trace/runtime"

export function usePageTrace(pageKey: string) {

  // start
  useEffect(() => {
    const existing = traceRuntime.current()

    if (!existing) {
      traceRuntime.start({
        page: pageKey,
        trigger: "mount",
        rootName: "page_pipeline",
        meta: { page: pageKey },
      })
    }
  }, [pageKey])

  // finish
  useEffect(() => {
    return () => {
      const active = traceRuntime.current()
      if (active) {
        traceRuntime.finishOk({
          stage: "page_unmount",
        })
      }
    }
  }, [pageKey])
}