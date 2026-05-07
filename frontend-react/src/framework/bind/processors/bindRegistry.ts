// src/framework/bind/processors/bindRegistry.ts

import type { BindScope, AnyBlock } from "../types"

export type BindProcessor = (
  block: AnyBlock,
  scope: BindScope
) => AnyBlock | null

const processors: BindProcessor[] = []

export function registerBindProcessor(
  processor: BindProcessor
): void {
  processors.push(processor)
}

export function runBindProcessors<T extends object>(
  block: T,
  scope: BindScope
): T | null {
  let current: AnyBlock | null = block as AnyBlock

  for (const processor of processors) {
    if (!current) return null
    current = processor(current, scope)
  }

  return current as T | null
}