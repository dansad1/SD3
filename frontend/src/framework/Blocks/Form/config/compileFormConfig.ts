import type { FormApiBlock } from "../types/api"
import type { FormConfig } from "../types/FormConfig"

// compileFormConfig.ts

export function compileFormConfig(block: FormApiBlock): FormConfig {
  if ("entity" in block) {
    return {
      formType: "entity",
      entity: block.entity,

      // ❗ НЕ задаём дефолт
      mode: block.mode,

      objectId: block.objectId,
      initial: block.initial,
      formLayout: block.formLayout,
      submit: block.submit,
    }
  }

  return {
    formType: "action",
    schema: block.schema,
    formLayout: block.formLayout,
    submit:
      typeof block.submit === "string"
        ? { action: block.submit }
        : block.submit,
  }
}