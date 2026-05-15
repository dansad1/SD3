// src/framework/BlockRenderer.tsx

import React from "react"

import { blockRegistry } from "./BlockRegistry"

import type { PageBlock }
  from "../../page/PageSchema"
import { CapabilityBoundary } from "@/framework/security/CapabilityBoundary"


export function BlockRenderer({
  block,
  children,
}: {
  block: PageBlock
  children?: React.ReactNode
}) {

  const Component =
    blockRegistry.get(block.type)

  if (!Component) {
    console.error(
      "No renderer for block:",
      block.type,
      block
    )

    return (
      <div
        style={{
          border: "1px solid red",
          padding: 8,
        }}
      >
        Unknown block:
        <b>{String(block.type)}</b>
      </div>
    )
  }

  const nested =
    "blocks" in block &&
    Array.isArray(block.blocks)
      ? block.blocks.map((child, i) => (
          <BlockRenderer
            key={
              child.id ??
              `${child.type}-${i}`
            }
            block={child}
          />
        ))
      : children

  return (
    <CapabilityBoundary
      capabilities={block.capabilities}
    >
      <Component block={block}>
        {nested}
      </Component>
    </CapabilityBoundary>
  )
}