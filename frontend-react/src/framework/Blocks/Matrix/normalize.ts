import { normalizeId, normalizeLayout } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type MatrixApiBlock = Extract<ApiPageBlock, { type: "matrix" }>

export function normalizeMatrix(
  block: MatrixApiBlock
): MatrixApiBlock {
  return {
    ...block,
    id: normalizeId(block.id),
    layout: normalizeLayout(block.layout),
  }
}