import {
  useRef,
  useEffect,
} from "react"

import { usePageDirty }
  from "../../hooks/usePageDirty"

import { useFormRuntime }
  from "../runtime/useFormRuntime"

import type {
  FormConfig,
  FormEntityConfig,
  FormActionConfig,
} from "../types/FormConfig"

export function useFormController(
  config: FormConfig
) {

  /* ==================================================== */
  /* FORM RUNTIME */
  /* ==================================================== */

  const form =
    useFormRuntime(config)

  /* ==================================================== */
  /* SUBMIT REF */
  /* ==================================================== */

  const submitRef =
    useRef(form.submit)

  useEffect(() => {

    submitRef.current =
      form.submit

  }, [form.submit])

  /* ==================================================== */
  /* FORM ID */
  /* ==================================================== */

  const formId = (() => {

    if (config.formType === "entity") {

      const entityConfig =
        config as FormEntityConfig

      return entityConfig.objectId

        ? `form:${entityConfig.entity}:${entityConfig.objectId}`

        : `form:${entityConfig.entity}:create`
    }

    const actionConfig =
      config as FormActionConfig

    return `action-form:${actionConfig.schema}`

  })()

  /* ==================================================== */
  /* DIRTY STATE */
  /* ==================================================== */

  usePageDirty(
    formId,
    form.dirty
  )

  /* ==================================================== */
  /* FORM API */
  /* ==================================================== */

  useEffect(() => {

   

    // ==================================================
    // REGISTER
    // ==================================================

    

    // ==================================================
    // CLEANUP
    // ==================================================

    return () => {

    }

  }, [

    formId,

    form.values,

    form.dirty,

  ])

  /* ==================================================== */
  /* RETURN */
  /* ==================================================== */

  return {

    ...form,

    formId,

  }
}