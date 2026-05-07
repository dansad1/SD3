import type { PageBlock } from "@/framework/page/PageSchema"

const layoutTypes = new Set([
  "container",
  "stack",
  "section",
  "split",
  "if",
])

export function isLayoutBlock(
  block: PageBlock
): block is Extract<PageBlock, { blocks?: PageBlock[] }> {
  return layoutTypes.has(block.type)
}