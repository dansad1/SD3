// src/framework/Blocks/Data/normalize.ts

import { normalizeId } from "@/framework/normalize/normalizeCommon"
import { dispatchNormalize } from "@/framework/normalize/normalizeDispatch"
import type { ResourceBlock } from "../types"


export function normalizeResource(
  block: ResourceBlock
): ResourceBlock {

  return {
    ...block,

    id: normalizeId(block.id),

    blocks: block.blocks?.map(dispatchNormalize) ?? [],
  }
}