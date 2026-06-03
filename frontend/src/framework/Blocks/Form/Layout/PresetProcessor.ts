import { registerFormLayoutProcessor } from "./registry"
import { mapBlocks } from "./walk"

import type { FormBlock } from "../types/types"
import type { FormLayoutConfig } from "../types/FormConfig"

type Span =
  | 1
  | 2
  | 3
  | 4
  | 6
  | 12

function getPresetSpan(
  preset: string
): Span {

  switch (preset) {

    case "single-column":
      return 12

    case "two-columns":
      return 6

    case "wide":
      return 4

    default:
      return 6
  }
}

function adjustByType(
  block: FormBlock,
  span: Span
): Span {

  if (block.type !== "field") {
    return span
  }

  const field = block.field

  if (
    field.widget === "textarea" ||
    field.type === "text"
  ) {
    return 12
  }

  if (
    field.widget === "checkbox" ||
    field.type === "boolean"
  ) {
    return span <= 3
      ? span
      : 3
  }

  return span
}

export function presetProcessor(
  blocks: FormBlock[],
  layout: FormLayoutConfig
): FormBlock[] {

  const preset =
    layout.preset ?? "default"

  const presetSpan =
    getPresetSpan(preset)

  return mapBlocks(
    blocks,
    (
      block: FormBlock
    ): FormBlock => {

      if (
        block.type !== "field"
      ) {
        return block
      }

      // backend задал span
      if (
        block.layout?.span
      ) {
        return block
      }

      return {
        ...block,

        layout: {
          ...(block.layout ?? {}),

          span: adjustByType(
            block,
            presetSpan
          ),
        },
      }
    }
  )
}

registerFormLayoutProcessor(
  presetProcessor
)