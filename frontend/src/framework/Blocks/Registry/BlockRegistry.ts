import type { PageBlock } from "@/framework/page/PageSchema"
import type { FC, ReactNode } from "react"

/* =========================================================
   TYPE HELPERS
   ========================================================= */

type PageBlockByType = {
  [K in PageBlock["type"]]: Extract<PageBlock, { type: K }>
}

export type BlockComponent<T extends PageBlock["type"]> =
  FC<{
    block: PageBlockByType[T]
    children?: ReactNode
  }>

/* =========================================================
   REGISTRY (RENDER ONLY)
   ========================================================= */

class BlockRegistry {
  private map = new Map<
    PageBlock["type"],
    BlockComponent<PageBlock["type"]>
  >()

  register<T extends PageBlock["type"]>(
    type: T,
    component: BlockComponent<T>
  ) {
    if (this.map.has(type)) {
      throw new Error(`Block "${type}" already registered`)
    }

    this.map.set(
      type,
      component as BlockComponent<PageBlock["type"]>
    )
  }

  get<T extends PageBlock["type"]>(
    type: T
  ): BlockComponent<T> {
    const component = this.map.get(type)

    if (!component) {
      throw new Error(`Unknown block type: ${type}`)
    }

    return component as BlockComponent<T>
  }

  has(type: PageBlock["type"]) {
    return this.map.has(type)
  }

  getAllTypes(): PageBlock["type"][] {
    return Array.from(this.map.keys())
  }
}

export const blockRegistry = new BlockRegistry()