// src/framework/Blocks/Form/Layout/normalize.ts

import { normalizeId, normalizeLayout } from "@/framework/normalize/normalizeCommon"
import type { FormApiBlock } from "../types/api"

/**
 * Form — leaf block.
 * Не является layout-контейнером.
 */
export function normalizeForm(
  block: FormApiBlock
): FormApiBlock {
  return {
    ...block,
    id: normalizeId(block.id),
    layout: normalizeLayout(block.layout),
  }
}