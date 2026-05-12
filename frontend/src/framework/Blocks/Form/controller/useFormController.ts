import { useMemo } from "react"
import { usePageAction } from "../../Action/usePageAction"
import { usePageDirty } from "../../hooks/usePageDirty"
import { useFormRuntime } from "../runtime/useFormRuntime"
import type { FormActionConfig, FormConfig, FormEntityConfig } from "../types/FormConfig"

export function useFormController(config: FormConfig) {
  const form = useFormRuntime(config)
  const isEntity = config.formType === "entity"

  /* ================= ACTION ID ================= */

  const actionId = useMemo(() => {
    if (config.formType === "entity") {
      const entityConfig = config as FormEntityConfig

      const scope = entityConfig.objectId
        ? `${entityConfig.entity}:${entityConfig.objectId}`
        : `${entityConfig.entity}:create`

      return `form:${scope}`
    }

    const actionConfig = config as FormActionConfig
    return `action-form:${actionConfig.schema}`
  }, [config])

  /* ================= DIRTY ================= */

  usePageDirty(actionId, form.dirty)

  /* ================= LABEL ================= */

  const label = isEntity
    ? (config as FormEntityConfig).submit?.label ?? "Сохранить"
    : "Отправить"

  /* ================= RUN ================= */

  const run = async () => {
    console.log("🚀 FORM SUBMIT", form.values)
    return await form.submit()
  }

  /* ================= REGISTER ================= */

 usePageAction(actionId, {
  id: actionId,
  order: 10,
  label,
  placement: "form", // 🔥 ключ
  validate: () => true,
  run,
})

  return form
}