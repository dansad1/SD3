// src/framework/physical/render/PhysicalNodeRenderer.tsx

import { BlockShell }
  from "@/framework/Blocks/Registry/BlockShell"

import { BlockRenderer }
  from "@/framework/Blocks/Registry/BlockRenderer"

import type { PhysicalNode }
  from "../types/PhysicalNode"

export function PhysicalNodeRenderer({
  node,
}: {
  node: PhysicalNode
}) {

  if (node.kind === "grid-item") {

    if (node.layout.hidden) {
      return null
    }

    return (
      <BlockShell layout={node.layout}>
        <BlockRenderer block={node.block} />
      </BlockShell>
    )
  }

  return (
    <BlockRenderer block={node.block}>
      {node.children.map(child => (
        <PhysicalNodeRenderer
          key={child.id}
          node={child}
        />
      ))}
    </BlockRenderer>
  )
}