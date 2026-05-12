import { useMemo, useState } from "react"

export function useChangeSet<T>(initial: T | null) {
  const [original, setOriginal] = useState<T | null>(initial)
  const [current, setCurrent] = useState<T | null>(initial)

  const hasChanges = useMemo(
    () => JSON.stringify(original) !== JSON.stringify(current),
    [original, current]
  )

  const commit = () => setOriginal(current)
  const reset = () => setCurrent(original)

  return { original, current, setCurrent, hasChanges, commit, reset }
}
