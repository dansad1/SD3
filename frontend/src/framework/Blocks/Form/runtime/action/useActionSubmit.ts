import { useCallback } from "react"

import { submitAction }
  from "@/framework/api/action/submitAction"

import { parseApiError }
  from "@/framework/utils/parseApiError"

import { usePageApi }
  from "@/framework/page/context/usePageApi"

import type { FormState }
  from "../base/useFormState"

type Params = {

  code?: string

  state: FormState
}

export function useActionSubmit({
  code,
  state,
}: Params) {

  const page =
    usePageApi()

  return useCallback(async () => {

    /* ========================================== */
    /* GUARDS */
    /* ========================================== */

    if (

      !code ||

      state.saving ||

      state.readonly

    ) {

      return false
    }

    /* ========================================== */
    /* PAYLOAD */
    /* ========================================== */

    const payload =
      state.buildPayload("all")

    console.log(
      "📤 FORM PAYLOAD",
      payload
    )

    /* ========================================== */
    /* PREPARE */
    /* ========================================== */

    state.setSaving(true)

    state.setFormError(null)

    state.setFieldErrors({})

    try {

      /* ======================================== */
      /* SUBMIT */
      /* ======================================== */

      const result =
        await submitAction(
          code,
          payload
        )

      console.log(
        "✅ ACTION RESULT",
        result
      )

      /* ======================================== */
      /* EFFECTS */
      /* ======================================== */

      if (result.effects) {

        console.log(
          "⚡ RUN EFFECTS",
          result.effects
        )

        // 🔥 CRITICAL
        await page.runEffects(
          result.effects
        )
      }

      /* ======================================== */
      /* LEGACY REDIRECT */
      /* ======================================== */

      if (result.redirect) {

        await page.runEffect({

          type: "navigate",

          page: result.redirect,

        })
      }

      /* ======================================== */
      /* MESSAGE */
      /* ======================================== */

      if (result.message) {

        await page.runEffect({

          type: "toast",

          variant:

            result.status === "ok"

              ? "success"

              : "info",

          message:
            result.message,

        })
      }

      /* ======================================== */
      /* RESET DIRTY */
      /* ======================================== */

      state.resetDirty()

      return (
        result.status === "ok"
      )

    } catch (e) {

      console.error(
        "❌ ACTION SUBMIT ERROR",
        e
      )

      const err =
        parseApiError(e)

      console.log(
        "🧨 PARSED ERROR",
        err
      )

      /* ======================================== */
      /* FIELD ERRORS */
      /* ======================================== */

      if (err.field_errors) {

        state.setFieldErrors(
          err.field_errors
        )
      }

      /* ======================================== */
      /* FORM ERROR */
      /* ======================================== */

      state.setFormError(
        err.message
      )

      /* ======================================== */
      /* TOAST */
      /* ======================================== */

      await page.runEffect({

        type: "toast",

        variant: "error",

        message: err.message,

      })

      return false

    } finally {

      state.setSaving(false)
    }

  }, [

    code,

    state,

    page,

  ])
}