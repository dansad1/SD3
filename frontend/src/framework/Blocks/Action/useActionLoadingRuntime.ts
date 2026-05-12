import { useCallback, useRef, useSyncExternalStore } from "react"

export function usePageLoadingRuntime() {
  const runningRef = useRef<Set<string>>(new Set())

  const subscribe = (callback: () => void) => {
    // простой pub/sub
    const interval = setInterval(callback, 50)
    return () => clearInterval(interval)
  }

  const getSnapshot = () => runningRef.current

  useSyncExternalStore(subscribe, getSnapshot)

  const start = useCallback((id: string) => {
    if (runningRef.current.has(id)) {
      return false
    }

    runningRef.current.add(id)
    return true
  }, [])

  const finish = useCallback((id: string) => {
    runningRef.current.delete(id)
  }, [])

  const isRunning = useCallback((id: string) => {
    return runningRef.current.has(id)
  }, [])

  return {
    start,
    finish,
    isRunning,
  }
}