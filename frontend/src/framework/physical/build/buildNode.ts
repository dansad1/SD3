import type {
  Area,
  BlockLayout,
} from "@/framework/Blocks/BlockType"

import type {
  PageBlock,
} from "@/framework/page/PageSchema"

import {
  ensureId,
  getBlockLayout,
  getBlockChildren,
} from "./helpers"

import type {
  PhysicalNode,
} from "../types/PhysicalNode"

import {
  isLayoutBlock,
} from "../utils/isLayoutBlock"

export function buildNode(
  block: PageBlock,
  order: number,
  inheritedArea: Area,
  path: string = "0"
): PhysicalNode {

  const blockLayout =
    getBlockLayout(block)

  const area =
    blockLayout?.area ??
    inheritedArea

  const layout: Required<BlockLayout> = {
    area,
    span: blockLayout?.span ?? 12,
    order: blockLayout?.order ?? order,
    hidden: blockLayout?.hidden ?? false,
  }

  if (isLayoutBlock(block)) {

    const children =
      getBlockChildren(block)

    return {
      kind: "layout",

      id: ensureId(
        block.id,
        `layout-${path}`
      ),

      block,
      layout,

      children: children.map((child, i) =>
        buildNode(
          child,
          i,
          area,
          `${path}.${i}`
        )
      ),
    }
  }

  return {
    kind: "grid-item",

    id: ensureId(
      block.id,
      `item-${path}`
    ),

    block,
    layout,
  }
}