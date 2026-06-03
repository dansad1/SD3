// Layout/walk.ts

import type { FormBlock } from "../types/types"

export function mapBlocks(
  blocks: FormBlock[],
  mapper: (block: FormBlock) => FormBlock
): FormBlock[] {

  return blocks.map(block => {

    const next =
      mapper(block)

    if ("children" in next) {

      return {
        ...next,
        children: mapBlocks(
          next.children,
          mapper
        ),
      }
    }

    return next
  })
}