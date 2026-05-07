// src/framework/normalize/normalizeCommon.ts

import type { BlockLayout } from "../Blocks/BlockType"


export function normalizeId(
  id?: string | number
): string | undefined {
  return id == null ? undefined : String(id)
}

export function normalizeLayout(
  layout?: BlockLayout
): BlockLayout | undefined {
  if (!layout) return undefined

  return {
    area: layout.area,
    order: layout.order,
    span: layout.span,
    hidden: layout.hidden ?? false,
  }
}