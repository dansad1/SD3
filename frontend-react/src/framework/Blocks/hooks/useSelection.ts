import { useCallback, useMemo, useState } from "react"

export function useSelection<T extends { id: string | number }>(
  items: T[],
  enabled: boolean
) {
  const [selected, setSelected] = useState<Set<string | number>>(new Set())

 const toggle = useCallback((id: string | number) => {
  setSelected(prev => {
    const next = new Set(prev)

    if (next.has(id)) {
      next.delete(id)
    } else {
      next.add(id)
    }

    return next
  })
}, [])

  const toggleAll = useCallback(() => {
    if (!enabled) return
    setSelected(
      prev =>
        prev.size === items.length
          ? new Set()
          : new Set(items.map(i => i.id))
    )
  }, [items, enabled])

  const clear = useCallback(() => setSelected(new Set()), [])

  const isAllSelected = useMemo(
    () => enabled && items.length > 0 && selected.size === items.length,
    [enabled, items, selected]
  )

  return { selected, toggle, toggleAll, clear, isAllSelected }
}
