import {
  useMemo,
  useCallback,
  useRef,
  useEffect,
} from "react"

import { usePageAction }
  from "../../Action/usePageAction"

import { usePageDirty }
  from "../../hooks/usePageDirty"

import { useFormRuntime }
  from "../runtime/useFormRuntime"

import type {
  FormActionConfig,
  FormConfig,
  FormEntityConfig,
} from "../types/FormConfig"

export function useFormController(
  config: FormConfig
) {

  /* ==================================================== */
  /* FORM */
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
  /* ACTION ID */
  /* ==================================================== */

  const actionId = useMemo(() => {

    if (config.formType === "entity") {

      const entityConfig =
        config as FormEntityConfig

      const scope =

        entityConfig.objectId

          ? `${entityConfig.entity}:${entityConfig.objectId}`

          : `${entityConfig.entity}:create`

      return `form:${scope}`
    }

    const actionConfig =
      config as FormActionConfig

    return `action-form:${actionConfig.schema}`

  }, [config])

  /* ==================================================== */
  /* DIRTY */
  /* ==================================================== */

  usePageDirty(
    actionId,
    form.dirty
  )

  /* ==================================================== */
  /* LABEL */
  /* ==================================================== */

  const label = useMemo(() => {

    const submit =
      config.submit

    if (

      submit &&

      typeof submit === "object" &&

      "label" in submit &&

      submit.label

    ) {

      return submit.label
    }

    if (config.formType === "entity") {

      return "Сохранить"
    }

    return "Отправить"

  }, [config])

  /* ==================================================== */
  /* RUN */
  /* ==================================================== */

  const run = useCallback(async () => {

    console.log(
      "🚀 FORM SUBMIT"
    )

    return await submitRef.current()

  }, [])

  /* ==================================================== */
  /* VALIDATE */
  /* ==================================================== */

  const validate = useCallback(() => {

    return true

  }, [])

  /* ==================================================== */
  /* ACTION HANDLER */
  /* ==================================================== */

  const actionHandler = useMemo(() => {

    return {

      id: actionId,

      order: 10,

      label,

      placement: "form" as const,

      validate,

      run,

    }

  }, [

    actionId,

    label,

    validate,

    run,

  ])

  /* ==================================================== */
  /* REGISTER ACTION */
  /* ==================================================== */

  usePageAction(
    actionId,
    actionHandler
  )

  /* ==================================================== */
  /* RETURN */
  /* ==================================================== */

  return form
}