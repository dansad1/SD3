import type { PageBlock } from "@/framework/page/PageSchema"
import { buildNode } from "./buildNode"
import type { PhysicalNode } from "../types/PhysicalNode"
import type { Area } from "@/framework/Blocks/BlockType"

export function buildPhysicalTree(
  blocks: PageBlock[],
  area: Area = "main"
): PhysicalNode {

  const rootBlock: PageBlock = {
    type: "container",
    blocks,
  }

  return {
    kind: "layout",
    id: "root",
    block: rootBlock,
    children: blocks.map((block, i) =>
      buildNode(block, i, area)
    ),
  }
}