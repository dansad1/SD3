import type { FormLayoutConfig } from "../types/FormConfig"
import { runFormLayoutProcessors } from "../Layout/registry"

// важно для регистрации
import "../Layout/PresetProcessor"
import type { FormSchema } from "../types/types"

export function applyLayoutConfig(
  schema: FormSchema,
  layout?: FormLayoutConfig
): FormSchema {

  if (!layout) {
    return schema
  }

  const processedBlocks = runFormLayoutProcessors(
    [...schema.blocks],
    layout
  )

  return {
    ...schema,
    blocks: processedBlocks,
  }
}