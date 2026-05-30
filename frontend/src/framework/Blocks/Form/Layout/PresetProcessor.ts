import { registerFormLayoutProcessor } from "./registry"
import type { FormBlock } from "../types/types"
import type { FormLayoutConfig } from "../types/FormConfig"

function getPresetSpan(
  preset: string
): number {

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
  span: number
): number {

  if (block.type !== "field") {
    return span
  }

  const field = block.field

  // textarea всегда широкая

  if (
    field.widget === "textarea" ||
    field.type === "text"
  ) {
    return 12
  }

  // чекбоксы компактнее

  if (
    field.widget === "checkbox" ||
    field.type === "boolean"
  ) {
    return Math.min(span, 3)
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

  return blocks.map(block => {

    if (block.type !== "field") {
      return block
    }

    // backend победил всех
    if (block.layout?.span) {
      return block
    }

    const finalSpan =
      adjustByType(
        block,
        presetSpan
      )

    return {
      ...block,
      layout: {
        ...(block.layout ?? {}),
        span: finalSpan,
      },
    }
  })
}

registerFormLayoutProcessor(
  presetProcessor
)