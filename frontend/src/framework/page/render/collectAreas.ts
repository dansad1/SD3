// src/framework/page/render/collectAreas.ts

import type {
  PhysicalNode,
  PhysicalLayoutNode,
} from "@/framework/physical/types/PhysicalNode"

export type AreaMap = {
  main: PhysicalNode[]
  "sidebar-left": PhysicalNode[]
  "sidebar-right": PhysicalNode[]
}

export function collectAreas(
  root: PhysicalLayoutNode
): AreaMap {

  const result: AreaMap = {
    main: [],
    "sidebar-left": [],
    "sidebar-right": [],
  }

  for (const child of root.children) {
    visit(child, result)
  }

  return result
}

function visit(
  node: PhysicalNode,
  result: AreaMap
) {

  const area =
    node.layout.area ?? "main"

  if (
    area === "sidebar-left" ||
    area === "sidebar-right"
  ) {
    result[area].push(node)
    return
  }

  if (node.kind === "layout") {
    for (const child of node.children) {
      visit(child, result)
    }
    return
  }

  result.main.push(node)
}