// layout/registry.ts

import type { FormLayoutConfig } from "../types/FormConfig"
import type { FormBlock } from "../types/types"

export type FormLayoutProcessor = (
  blocks: FormBlock[],
  layout: FormLayoutConfig
) => FormBlock[]

const processors: FormLayoutProcessor[] = []

export function registerFormLayoutProcessor(
  processor: FormLayoutProcessor
): void {
  processors.push(processor)
}

export function runFormLayoutProcessors(
  blocks: FormBlock[],
  layout: FormLayoutConfig
): FormBlock[] {
  let result = blocks

  for (const processor of processors) {
    result = processor(result, layout)
  }

  return result
}