import { traceRuntime } from "@/framework/trace/runtime"

export function traceStep<T>(
  name: string,
  pageId: string,
  meta: object,
  exec: () => T
): T {
  const trace = traceRuntime.current()

  if (!trace) return exec()

  return trace.stepSync(name, exec, {
    page: pageId,
    ...meta,
  })
}