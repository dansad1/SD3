import { registerFormLayoutProcessor } from "./registry"
import type { FormBlock } from "../types/types"
import type { FormLayoutConfig } from "../types/FormConfig"

function withSize(b: FormBlock, size: string): FormBlock {
  if (b.type !== "field") return b

  return {
    ...b,
    props: {
      ...(b.props ?? {}),
      size,
    },
  }
}

export function densityProcessor(
  blocks: FormBlock[],
  layout: FormLayoutConfig
): FormBlock[] {

  const density = layout.density ?? "default"

  switch (density) {
    case "compact":
      return blocks.map((b) => withSize(b, "sm"))

    case "dense":
      return blocks.map((b) => withSize(b, "xs"))

    case "comfortable":
      return blocks.map((b) => withSize(b, "md"))

    default:
      return blocks
  }
}

registerFormLayoutProcessor(densityProcessor)