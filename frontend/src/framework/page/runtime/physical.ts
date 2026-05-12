import { useMemo } from "react"
import { traceStep } from "./trace"

import type { ApiPageBlock } from "../PageSchema"
import type { PhysicalNode } from "@/framework/physical/types/PhysicalNode"
import { buildPhysicalTree } from "@/framework/physical/build/buildPhysicalTree"

export function usePhysical(
  blocks: ApiPageBlock[],
  pageId: string
): PhysicalNode | null {
  return useMemo(() => {
    return traceStep(
      "build_physical_tree",
      pageId,
      { stage: "physical", nodes: blocks.length },
      () => buildPhysicalTree(blocks)
    )
  }, [blocks, pageId])
}