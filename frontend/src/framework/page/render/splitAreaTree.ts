// src/framework/page/render/splitAreaTree.ts

import type {
  PhysicalNode,
  PhysicalLayoutNode,
} from "@/framework/physical/types/PhysicalNode"

export type AreaTrees = {
  main: PhysicalNode[]
  "sidebar-left": PhysicalNode[]
  "sidebar-right": PhysicalNode[]
}

export function splitAreaTree(
  root: PhysicalLayoutNode
): AreaTrees {

  return {

    main: buildMain(root),

    "sidebar-left":
      collectSidebar(
        root,
        "sidebar-left"
      ),

    "sidebar-right":
      collectSidebar(
        root,
        "sidebar-right"
      ),
  }
}

/* =====================================================
   MAIN TREE
   ===================================================== */

function buildMain(
  node: PhysicalNode
): PhysicalNode[] {

  if (
    node.layout.area ===
    "sidebar-left"
  ) {
    return []
  }

  if (
    node.layout.area ===
    "sidebar-right"
  ) {
    return []
  }

  if (
    node.kind ===
    "grid-item"
  ) {
    return [node]
  }

  const children =
    node.children.flatMap(
      buildMain
    )

  return [
    {
      ...node,
      children,
    },
  ]
}

/* =====================================================
   SIDEBAR TREE
   ===================================================== */

function collectSidebar(
  node: PhysicalNode,
  target:
    | "sidebar-left"
    | "sidebar-right"
): PhysicalNode[] {

  const result: PhysicalNode[] = []

  visit(
    node,
    target,
    result
  )

  return result
}

function visit(
  node: PhysicalNode,
  target:
    | "sidebar-left"
    | "sidebar-right",

  result: PhysicalNode[]
) {

  if (
    node.layout.area === target
  ) {

    result.push(node)

    return
  }

  if (
    node.kind === "layout"
  ) {

    node.children.forEach(
      child =>
        visit(
          child,
          target,
          result
        )
    )
  }
}