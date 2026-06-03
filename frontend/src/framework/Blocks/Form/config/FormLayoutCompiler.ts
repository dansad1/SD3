import type {
  FormLayoutConfig,
} from "../types/FormConfig"

import type {
  FormBlock,
  FormSchema,
} from "../types/types"

import {
  runFormLayoutProcessors,
} from "../Layout/registry"

import "../Layout/PresetProcessor"
import "../Layout/DensityProcessor"

import {
  compileSchemaBlocks,
} from "../render/compileSchemaBlocks"

export type CompiledFormSchema =
  FormSchema & {
    blocks: FormBlock[]
  }

export function applyLayoutConfig(
  schema: FormSchema,
  layout?: FormLayoutConfig
): CompiledFormSchema {

  const schemaWithLayout: FormSchema = {
    ...schema,

    layout: {
      ...(schema.layout ?? {}),

      preset:
        layout?.preset,

      density:
        layout?.density,

      groups:
        layout?.groups,
    },
  }

  const normalizedSchema =
    compileSchemaBlocks(
      schemaWithLayout
    )

  if (!layout) {
    return normalizedSchema
  }

  const processedBlocks =
    runFormLayoutProcessors(
      [...normalizedSchema.blocks],
      layout
    )

  return {
    ...normalizedSchema,

    layout: {
      ...(normalizedSchema.layout ?? {}),

      preset:
        layout.preset,

      density:
        layout.density,

      groups:
        layout.groups,
    },

    blocks:
      processedBlocks,
  }
}