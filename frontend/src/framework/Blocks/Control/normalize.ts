// framework/Blocks/control/normalize.ts

import { normalizeId } from "@/framework/normalize/normalizeCommon"
import { dispatchNormalize } from "@/framework/normalize/normalizeDispatch"

import type { ForBlock, IfBlock } from "./types"

export function normalizeIf(
  block: IfBlock
): IfBlock {
  return {
    ...block,
    id: normalizeId(block.id),
    blocks: (block.blocks ?? []).map(dispatchNormalize),
  }
}

export function normalizeFor(
  block: ForBlock
): ForBlock {
  console.log("NORMALIZE FOR INPUT", block)

  return {
    ...block,
    id: normalizeId(block.id),
    blocks: (block.blocks ?? []).map(dispatchNormalize),
  }
}