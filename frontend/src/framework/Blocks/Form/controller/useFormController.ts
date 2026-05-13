import { useMemo } from "react"

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

  // =====================================================
  // FORM
  // =====================================================

  const form =
    useFormRuntime(config)

 

  // =====================================================
  // ACTION ID
  // =====================================================

  const actionId = useMemo(() => {

    // ===================================================
    // ENTITY FORM
    // ===================================================

    if (config.formType === "entity") {

      const entityConfig =
        config as FormEntityConfig

      const scope =
        entityConfig.objectId

          ? `${entityConfig.entity}:${entityConfig.objectId}`

          : `${entityConfig.entity}:create`

      return `form:${scope}`
    }

    // ===================================================
    // ACTION FORM
    // ===================================================

    const actionConfig =
      config as FormActionConfig

    return `action-form:${actionConfig.schema}`

  }, [config])

  // =====================================================
  // DIRTY
  // =====================================================

  usePageDirty(
    actionId,
    form.dirty
  )

  // =====================================================
  // LABEL
  // =====================================================

  function getSubmitLabel(
    config: FormConfig
  ) {

    const submit =
      config.submit

    // ===============================================
    // CUSTOM LABEL
    // ===============================================

    if (

      submit &&

      typeof submit === "object" &&

      "label" in submit &&

      submit.label

    ) {

      return submit.label
    }

    // ===============================================
    // ENTITY DEFAULT
    // ===============================================

    if (config.formType === "entity") {

      return "Сохранить"
    }

    // ===============================================
    // ACTION DEFAULT
    // ===============================================

    return "Отправить"
  }

  const label =
    getSubmitLabel(config)

  // =====================================================
  // RUN
  // =====================================================

  const run = async () => {

    console.log(
      "🚀 FORM SUBMIT",
      form.values
    )

    return await form.submit()
  }

  // =====================================================
  // REGISTER ACTION
  // =====================================================

  usePageAction(actionId, {

    id: actionId,

    order: 10,

    label,

    placement: "form",

    validate: () => true,

    run,
  })

  // =====================================================
  // RETURN
  // =====================================================

  return form
}