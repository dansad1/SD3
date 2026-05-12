import { useEffect } from "react"
import { loadActionSchema } from "@/framework/api/action/loadActionSchema"
import { parseApiError } from "@/framework/utils/parseApiError"
import { adaptFormSchema } from "../../config/adaptFormSchema"
import type { FormState } from "../base/useFormState"

type Params = {
  schema?: string
  state: FormState
}

export function useActionLoader({ schema, state }: Params) {
  useEffect(() => {
    if (!schema) {
      state.setLoading(false)
      return
    }

    let cancelled = false

    const run = async () => {
      state.setLoading(true)
      state.setFormError(null)

      try {
        const api = await loadActionSchema(schema)
        if (cancelled) return

        const ui = adaptFormSchema(api)
        state.setSchema(ui)
        state.setInitialValues(ui.initial ?? {})
      } catch (e) {
        const err = parseApiError(e)
        state.setFormError(err.message)
      } finally {
        if (!cancelled) {
          state.setLoading(false)
        }
      }
    }

    run()

    return () => {
      cancelled = true
    }
  }, [schema]) // eslint-disable-line react-hooks/exhaustive-deps
}