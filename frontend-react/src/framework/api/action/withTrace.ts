// src/framework/api/action/withTrace.ts

import { traceRuntime } from "@/framework/trace/runtime"

type TraceMeta = {
  stage: string
  action: string
  block: string
  [key: string]: unknown
}

export function withTrace<T>(
  stepName: string,
  exec: () => Promise<T>,
  meta: TraceMeta
): Promise<T> {
  const trace = traceRuntime.current()

  if (!trace) {
    return exec()
  }

  return trace.step<T>(stepName, exec, meta)
}