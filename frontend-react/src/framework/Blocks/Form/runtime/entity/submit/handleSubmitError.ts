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
  const err = parseApiError(error)

  console.error("❌ SUBMIT ERROR", err)

  if (err.field_errors) {
    state.setFieldErrors(err.field_errors)
  }

  const message = getApiErrorMessage(err)

  state.setFormError(message)

  await page.runEffect({
    type: "toast",
    variant: "error",
    message,
  })
}