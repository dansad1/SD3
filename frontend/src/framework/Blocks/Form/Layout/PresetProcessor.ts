import { registerFormLayoutProcessor } from "./registry"
import type { FormBlock } from "../types/types"
import type { FormLayoutConfig } from "../types/FormConfig"

function withSpan(b: FormBlock, span: number): FormBlock {
  if (b.type !== "field") return b

  return {
    ...b,
    layout: {
      ...(b.layout ?? {}),
      span,
    },
  }
}

export function presetProcessor(
  blocks: FormBlock[],
  layout: FormLayoutConfig
): FormBlock[] {

  const preset = layout.preset ?? "default"

  switch (preset) {
    case "single-column":
      return blocks.map((b) => withSpan(b, 12))

    case "two-columns":
      return blocks.map((b) => withSpan(b, 6))

    case "wide":
      return blocks.map((b) => withSpan(b, 12))

    default:
      return blocks
  }
}

registerFormLayoutProcessor(presetProcessor)