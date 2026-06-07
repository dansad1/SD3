import type { PageBlock }
  from "@/framework/page/PageSchema"

import type { Area }
  from "@/framework/Blocks/BlockType"

import { buildNode }
  from "./buildNode"

import type {
  PhysicalNode,
} from "../types/PhysicalNode"

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

    layout: {
      area,
      span: 12,
      order: 0,
      hidden: false,
    },

    children: blocks.map((block, i) =>
      buildNode(
        block,
        i,
        area,
        String(i)
      )
    ),
  }
}