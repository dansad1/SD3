// src/framework/physical/PhysicalNode.ts

import type { BlockLayout } from "../../Blocks/BlockType"
import type { PageBlock } from "../../page/PageSchema"



export type PhysicalNode =
  | PhysicalLayoutNode
  | PhysicalGridItemNode

export type PhysicalLayoutNode = {
  kind: "layout"
  id: string
  block: PageBlock
  children: PhysicalNode[]
}

export type PhysicalGridItemNode = {
  kind: "grid-item"
  id: string
  block: PageBlock
  layout: Required<BlockLayout>
}
export type PhysicalBlock = {
  id: string
  content: PageBlock
  layout: Required<BlockLayout>
}
