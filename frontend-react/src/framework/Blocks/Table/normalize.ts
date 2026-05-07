import { normalizeId, normalizeLayout } from "@/framework/normalize/normalizeCommon"
import type { TableApiBlock } from "./types/api"

export function normalizeTable(
  block: TableApiBlock
): TableApiBlock {
  return {
    ...block,
    id: normalizeId(block.id),
    layout: normalizeLayout(block.layout),
  }
}