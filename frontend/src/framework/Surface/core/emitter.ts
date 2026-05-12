export function createEmitter() {
  const listeners = new Set<() => void>()

  return {
    emit() {
      listeners.forEach(fn => fn())
    },
    subscribe(fn: () => void) {
      listeners.add(fn)
      return () => listeners.delete(fn)
    },
  }
}