import { useCallback } from "react"
import { traceRuntime } from "@/framework/trace/runtime"

export function useFormSubmit(deps: {
  saving: boolean
  readonly: boolean
  setSaving: (v: boolean) => void
  setFormError: (v: string | null) => void
  setFieldErrors: (v: Record<string, string>) => void
}) {
  const {
    saving,
    readonly,
    setSaving,
    setFormError,
    setFieldErrors,
  } = deps

  return useCallback(async (
    payload: Record<string, unknown>,
    submitFn: (p: Record<string, unknown>) => Promise<void>
  ) => {

    if (saving || readonly) return false

    const trace = traceRuntime.current()

    const exec = async () => {

      setSaving(true)
      setFormError(null)
      setFieldErrors({})

      try {
        await submitFn(payload)
        return true
      } catch (e) {
        setFormError("Ошибка сохранения")
        throw e
      } finally {
        setSaving(false)
      }

    }

    if (!trace) {
      try {
        return await exec()
      } catch {
        return false
      }
    }

    try {
      return await trace.step("form_submit_runtime", exec)
    } catch {
      return false
    }

  }, [
    saving,
    readonly,
    setSaving,
    setFormError,
    setFieldErrors,
  ])
}