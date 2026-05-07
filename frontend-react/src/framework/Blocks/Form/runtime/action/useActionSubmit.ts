import { useCallback } from "react"
import { submitAction } from "@/framework/api/action/submitAction"
import { parseApiError } from "@/framework/utils/parseApiError"
import { usePageApi } from "@/framework/page/context/usePageApi"
import type { FormState } from "../base/useFormState"

type Params = {
  code?: string
  state: FormState
}

export function useActionSubmit({
  code,
  state,
}: Params) {
  const page = usePageApi()

  return useCallback(async () => {
    if (!code || state.saving || state.readonly) {
      return false
    }

    const payload = state.buildPayload("all")

    state.setSaving(true)
    state.setFormError(null)
    state.setFieldErrors({})

    try {
      const result = await submitAction(
        code,
        payload
      )

      if (result.effects) {
        page.runEffects(result.effects)
      }

      if (result.redirect) {
        page.runEffect({
          type: "navigate",
          page: result.redirect,
        })
      }

      if (result.message) {
        page.runEffect({
          type: "toast",
          variant:
            result.status === "ok"
              ? "success"
              : "info",
          message: result.message,
        })
      }

      state.resetDirty()

      return result.status === "ok"
    } catch (e) {
      const err = parseApiError(e)

      if (err.field_errors) {
        state.setFieldErrors(err.field_errors)
      }

      state.setFormError(err.message)

      page.runEffect({
        type: "toast",
        variant: "error",
        message: err.message,
      })

      return false
    } finally {
      state.setSaving(false)
    }
  }, [code, state, page])
}