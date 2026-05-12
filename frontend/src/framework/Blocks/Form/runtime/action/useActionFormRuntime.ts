import type { FormActionConfig } from "../../types/FormConfig"

import { useFormState } from "../base/useFormState"

import { useActionLoader } from "./useActionLoader"
import { useActionSubmit } from "./useActionSubmit"

import type { FormSchema } from "../../types/types"
import { useFormReactions } from "../reactions/useFormReactions"

export function useActionFormRuntime(
  params: FormActionConfig | null
) {
  const state = useFormState<FormSchema>()

  /* ================= LOAD ================= */

  useActionLoader({
    schema: params?.schema,
    state,
  })

  /* ================= 🔥 REACTIONS ================= */

  useFormReactions({ state })

  /* ================= SUBMIT ================= */

  const submitCode =
    typeof params?.submit === "string"
      ? params.submit
      : params?.submit?.action

  const submit = useActionSubmit({
    code: submitCode,
    state,
  })

  /* ================= VALIDATE ================= */

  const validate = () => {
    // action формы могут быть всегда валидны,
    // либо позже можно сюда добавить dynamic validation rules
    return true
  }

  /* ================= RETURN ================= */

  return {
    ...state,
    submit,
    validate,
  }
}