import { useCallback, useRef, useState } from "react"

export function usePageDirtyRuntime() {
  const dirtyRef = useRef<Record<string, boolean>>({})
  const [pageDirty, setPageDirty] = useState(false)

  const recomputeDirty = useCallback(() => {
    const dirty = Object.values(dirtyRef.current).some(Boolean)

    setPageDirty(prev => (prev === dirty ? prev : dirty))
  }, [])

  const setDirty = useCallback(
    (sourceId: string, dirty: boolean) => {
      if (dirty) {
        dirtyRef.current[sourceId] = true
      } else {
        delete dirtyRef.current[sourceId]
      }

      recomputeDirty()
    },
    [recomputeDirty]
  )

  const unregisterDirty = useCallback(
    (sourceId: string) => {
      if (!(sourceId in dirtyRef.current)) {
        return
      }

      delete dirtyRef.current[sourceId]
      recomputeDirty()
    },
    [recomputeDirty]
  )

  const getPageDirty = useCallback(() => {
    return Object.values(dirtyRef.current).some(Boolean)
  }, [])

  return {
    pageDirty,
    setDirty,
    unregisterDirty,
    getPageDirty,
  }
}