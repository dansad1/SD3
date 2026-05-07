import { useMemo } from "react"
import { usePageLoadingRuntime } from "@/framework/Blocks/Action/useActionLoadingRuntime"

export function usePageLoadingApi() {
  const {
    start,
    finish,
    isRunning,
  } = usePageLoadingRuntime()

  return useMemo(
    () => ({
      start,
      finish,
      isRunning,
    }),
    [start, finish, isRunning]
  )
}