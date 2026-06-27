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

import "../Layout/DensityProcessor"
import "../Layout/balanceRowsProcessor"

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

    const effectiveLayout: FormLayoutConfig = {

        strategy: "balance",

        ...(schema.layout ?? {}),

        ...(layout ?? {}),

    }


    const normalizedSchema =
        compileSchemaBlocks({

            ...schema,

            layout:

                effectiveLayout,

        })


    const processedBlocks =

        runFormLayoutProcessors(

            [...normalizedSchema.blocks],

            effectiveLayout

        )


    return {

        ...normalizedSchema,

        layout:

            effectiveLayout,

        blocks:

            processedBlocks,

    }

}