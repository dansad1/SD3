import { registerFormLayoutProcessor } from "./registry"
import { mapBlocks } from "./walk"

import type { FormBlock } from "../types/types"
import type { FormLayoutConfig } from "../types/FormConfig"

export function densityProcessor(
  blocks: FormBlock[],
  layout: FormLayoutConfig
): FormBlock[] {

  const density =
    layout.density ?? "default"

  return mapBlocks(
    blocks,
    (block): FormBlock => {

      if (block.type !== "field") {
        return block
      }

      return {
        ...block,

        field: {
          ...block.field,

          view: {
            ...(block.field.view ?? {}),

            density:
              density === "comfortable"
                ? "comfortable"
                : density === "compact"
                ? "compact"
                : density === "dense"
                ? "compact"
                : "normal",
          },
        },
      }
    }
  )
}

registerFormLayoutProcessor(
  densityProcessor
)