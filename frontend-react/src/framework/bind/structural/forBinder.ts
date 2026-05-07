// src/framework/bind/structural/forBinder.ts

import { registerStructuralBinder } from "./registry"
import type {
  BindScope,
  AnyBlock,
  BindResult,
} from "../types"

registerStructuralBinder({
  type: "for",

  bind(
    block: AnyBlock,
    scope: BindScope,
    bindChild
  ): BindResult {

    const itemKey =
      typeof block.as === "string" && block.as.length > 0
        ? block.as
        : "item"

    const localScope: BindScope = {
      ...scope,
      [itemKey]: undefined,
      $index: 0,
    }

    if (
      typeof block.index === "string" &&
      block.index.length > 0
    ) {
      localScope[block.index] = 0
    }

    return {
      ...block,

      blocks: Array.isArray(block.blocks)
        ? block.blocks
            .map(child => bindChild(child, localScope))
            .flat()
            .filter(Boolean)
        : [],

      children: Array.isArray(block.children)
        ? block.children
            .map(child => bindChild(child, localScope))
            .flat()
            .filter(Boolean)
        : [],
    }
  },
})