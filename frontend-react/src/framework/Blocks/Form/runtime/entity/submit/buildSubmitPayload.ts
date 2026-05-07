// form/hooks/submit/buildSubmitPayload.ts

import type { FormState } from "../../base/useFormState"


export function buildSubmitPayload(
  apiMode: "create" | "edit",
  state: FormState
) {
  if (apiMode === "create") {
    return state.buildPayload("all")
  }

  return state.buildPayload(
    state.dirty ? "dirty" : "all"
  )
}