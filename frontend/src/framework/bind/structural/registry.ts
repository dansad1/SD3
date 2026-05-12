// src/framework/bind/structural/registry.ts

import type { BindScope, AnyBlock, BindResult } from "../types"

export interface StructuralBinder {
  type: string
  bind: (
    block: AnyBlock,
    scope: BindScope,
    bindChild: (block: AnyBlock, scope: BindScope) => BindResult
  ) => BindResult | undefined
}

const structuralBinders: StructuralBinder[] = []

export function registerStructuralBinder(
  binder: StructuralBinder
) {
  structuralBinders.push(binder)
}

export function tryBindStructural(
  block: AnyBlock,
  scope: BindScope,
  bindChild: (block: AnyBlock, scope: BindScope) => BindResult
): BindResult | undefined {
  for (const binder of structuralBinders) {
    if (binder.type === block.type) {
      return binder.bind(block, scope, bindChild)
    }
  }
}