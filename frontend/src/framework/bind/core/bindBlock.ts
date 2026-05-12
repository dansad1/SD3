// src/framework/bind/core/bindBlock.ts

import type { BindScope, AnyBlock, BindResult } from "../types"
import { resolveProps } from "../expression/resolveProps"
import { runBindProcessors } from "../processors/bindRegistry"
import { tryBindStructural } from "../structural/registry"
import { bindChildren } from "./bindChildren"
import { traceRuntime } from "@/framework/trace/runtime"

function resolveBlockShallow(
  block: AnyBlock,
  scope: BindScope
): AnyBlock {
  const { children, blocks, ...rest } = block

  const resolved = resolveProps(rest, scope)
  const processed = runBindProcessors(resolved, scope)

  if (!processed) return block

  const out: AnyBlock = { ...processed }

  if (children !== undefined) out.children = children
  if (blocks !== undefined) out.blocks = blocks

  return out
}

export function bindBlock(
  block: AnyBlock,
  scope: BindScope
): BindResult {
  const trace = traceRuntime.current()

  const run = (): BindResult => {
    /* STRUCTURAL */
    const structural = tryBindStructural(
      block,
      scope,
      bindBlock
    )

    if (structural !== undefined) {
      return structural
    }

    /* NORMAL BLOCK */
    const resolved = resolveBlockShallow(
      block,
      scope
    )

    const processed = runBindProcessors(
      resolved,
      scope
    )

    if (!processed) return null

    const node: AnyBlock = { ...processed }

    // 🔥 for / if сами управляют своим внутренним scope
    // нельзя заранее биндить их children/blocks
    if (
      node.type === "for" ||
      node.type === "if"
    ) {
      return node
    }

    node.children = bindChildren(
      node.children,
      scope
    )

    node.blocks = bindChildren(
      node.blocks,
      scope
    )

    return node
  }

  if (!trace) return run()

  const type =
    typeof block.type === "string"
      ? block.type
      : "unknown"

  const result = trace.stepSync(
    `bind_block:${type}`,
    run,
    {
      stage: "bind_block",
      blockType: type,
    }
  )

  trace.annotate({
    before: block,
    after: result,
    changed: block !== result,
  })

  return result
}