import { normalizeId, normalizeLayout } from "@/framework/normalize/normalizeCommon"
import { dispatchNormalize } from "@/framework/normalize/normalizeDispatch"

import type { ApiPageBlock } from "@/framework/page/PageSchema"
import type { BlockLayout } from "../BlockType"

/* ================= TYPES ================= */

type ContainerApi = Extract<ApiPageBlock, { type: "container" }>
type SectionApi   = Extract<ApiPageBlock, { type: "section" }>
type StackApi     = Extract<ApiPageBlock, { type: "stack" }>
type SplitApi     = Extract<ApiPageBlock, { type: "split" }>

/* ================= GUARDS ================= */

function isApiPageBlockArray(x: unknown): x is ApiPageBlock[] {
  return Array.isArray(x)
}

/* ================= COMMON ================= */

function structuralCommon(block: {
  id?: string | number
  layout?: BlockLayout
  blocks?: unknown
}) {
  return {
    id: normalizeId(block.id),
    layout: normalizeLayout(block.layout),
    blocks: isApiPageBlockArray(block.blocks)
      ? block.blocks.map(dispatchNormalize)
      : [], // ✅ ВАЖНО
  }
}

/* ================= NORMALIZERS ================= */

export function normalizeContainer(
  block: ContainerApi
): ContainerApi {
  return {
    ...block,
    ...structuralCommon(block),
  }
}

export function normalizeSection(
  block: SectionApi
): SectionApi {
  return {
    ...block,
    ...structuralCommon(block),
  }
}

export function normalizeStack(
  block: StackApi
): StackApi {
  return {
    ...block,
    ...structuralCommon(block),
  }
}

export function normalizeSplit(
  block: SplitApi
): SplitApi {
  return {
    ...block,
    ...structuralCommon(block),
  }
}

