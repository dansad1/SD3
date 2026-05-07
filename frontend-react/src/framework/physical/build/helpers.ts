import type {  BlockLayout } from "@/framework/Blocks/BlockType"
import type { PageBlock } from "@/framework/page/PageSchema"

export function ensureId(
  id: PageBlock["id"] | undefined,
  fallback: string
): string {
  return id == null ? fallback : String(id)
}

export function getBlockLayout(
  block: PageBlock
): Partial<BlockLayout> | undefined {
  return "layout" in block ? block.layout : undefined
}

export function getBlockChildren(
  block: PageBlock
): PageBlock[] {
  if ("blocks" in block && Array.isArray(block.blocks)) {
    return block.blocks as PageBlock[]
  }
  return []
}