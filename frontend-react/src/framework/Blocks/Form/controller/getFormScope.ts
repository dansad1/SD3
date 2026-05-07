// src/framework/Blocks/Form/utils/getFormScope.ts

import type {
  FormConfig,
  FormEntityConfig,
  FormActionConfig,
} from "../types/FormConfig"

export function getFormScope(config: FormConfig) {
  if (config.formType === "entity") {
    const { entity, objectId } = config as FormEntityConfig

    const scope = objectId
      ? `${entity}:${objectId}`
      : `${entity}:create`

    return {
      scope,
      dataKey: scope,
      actionId: `form:${scope}`,
    }
  }

  const { schema } = config as FormActionConfig

  return {
    scope: schema,
    dataKey: `action:${schema}`,
    actionId: `action-form:${schema}`,
  }
}