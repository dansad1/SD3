import type { FormLayoutConfig } from "../types/FormConfig"
import { runFormLayoutProcessors } from "../Layout/registry"

import "../Layout/PresetProcessor"

import type { FormSchema } from "../types/types"

export function applyLayoutConfig(
  schema: FormSchema,
  layout?: FormLayoutConfig
): FormSchema {

  if (!layout) {
    return schema
  }

  const processedBlocks =
    runFormLayoutProcessors(
      [...schema.blocks],
      layout
    )

  return {
    ...schema,

    layout: {
      ...(schema.layout ?? {}),

      preset: layout.preset,

      density: layout.density,
    },

    blocks: processedBlocks,
  }
}