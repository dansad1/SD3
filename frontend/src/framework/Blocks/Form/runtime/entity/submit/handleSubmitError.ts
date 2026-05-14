// form/hooks/submit/handleSubmitError.ts

import { parseApiError } from "@/framework/utils/parseApiError"
import { getApiErrorMessage } from "@/framework/utils/ErrorMessage"
import type { PageApi } from "@/framework/page/context/types"
import type { FormState } from "../../base/useFormState"

export async function handleSubmitError(
  error: unknown,
  state: FormState,
  page: PageApi
) {

  const err =
    parseApiError(error)

  console.error(
    "❌ SUBMIT ERROR",
    err
  )

  // =====================
  // FIELD ERRORS
  // =====================

  if (err.field_errors) {

    state.setFieldErrors(
      err.field_errors
    )
  }

  // =====================
  // MESSAGE
  // =====================

  const message =
    getApiErrorMessage(err)

  // =====================
  // ONLY GLOBAL ERRORS
  // =====================

  const hasOnlyGlobalErrors =
    Boolean(
      err.field_errors?.__all__
    )

  if (hasOnlyGlobalErrors) {

    state.setFormError(message)

  } else {

    // field validation
    // НЕ пишем в form body

    state.setFormError(null)
  }

  // =====================
  // TOAST
  // =====================

  await page.runEffect({

    type: "toast",

    variant: "error",

    message,
  })
}