// src/framework/bind/core/bindChildren.ts

import type { AnyBlock, BindScope } from "../types"
import { bindBlock } from "./bindBlock"


export function bindChildren(
  nodes: unknown,
  scope: BindScope
): AnyBlock[] | undefined {
  if (!Array.isArray(nodes)) return undefined

  return nodes.flatMap((child) => {
    const result = bindBlock(child as AnyBlock, scope)
    if (!result) return []
    return Array.isArray(result) ? result : [result]
  })
}