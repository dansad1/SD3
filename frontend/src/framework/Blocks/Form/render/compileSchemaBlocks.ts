import type {
  ApiFormBlock,
  FormBlock,
  FormSchema,
} from "../types/types"

import type {
  FieldSchema,
} from "@/framework/components/dynamic/types"
import { buildBlocksFromFields, buildTabs, groupFieldBlocks } from "./groupFieldBlocks"
function hydrateApiBlock(
  block: ApiFormBlock,
  fieldMap: Map<
    string,
    FieldSchema
  >
): FormBlock | null {

  if (block.type === "field") {

    const field =
      fieldMap.get(
        block.field
      )

    if (!field) {
      return null
    }

    return {
      id:
        block.id ??
        `field.${block.field}`,

      type: "field",

      field,

      layout:
        block.layout,
    }
  }

  const children =
    (block.children ?? [])
      .map(child =>
        hydrateApiBlock(
          child,
          fieldMap
        )
      )
      .filter(
        (
          child
        ): child is FormBlock =>
          Boolean(child)
      )

  if (
    !children.length
  ) {
    return null
  }

  switch (block.type) {

    case "section":
      return {
        id:
          block.id ??
          `section.${
            block.key ??
            block.title ??
            "section"
          }`,

        type: "section",

        title:
          block.title,

        description:
          block.description,

        layout:
          block.layout,

        children,
      }

    case "stack":
      return {
        id:
          block.id ??
          "stack",

        type: "stack",

        gap:
          block.gap,

        layout:
          block.layout,

        children,
      }

    case "tabs":
      return {
        id:
          block.id ??
          "tabs",

        type: "tabs",

        variant:
          block.variant,

        layout:
          block.layout,

        children,
      }

    default:
      return null
  }
}

function isHydratedFormBlock(
  value: unknown
): value is FormBlock {

  if (
    !value ||
    typeof value !== "object"
  ) {
    return false
  }

  const block =
    value as Record<
      string,
      unknown
    >

  if (
    block.type === "field" &&
    typeof block.field === "object"
  ) {
    return true
  }

  return (
    ["section", "stack", "tabs"]
      .includes(
        String(block.type)
      ) &&
    Array.isArray(
      block.children
    )
  )
}

export function compileSchemaBlocks(
  schema: FormSchema
): FormSchema & {
  blocks: FormBlock[]
} {

  const fields =
    schema.fields ?? []

  const sourceBlocks =
    schema.blocks ?? []

  const groups =
    schema.layout?.groups

  /*
   * Уже гидратированные блоки
   */

  if (
    sourceBlocks.length > 0 &&
    sourceBlocks.every(
      isHydratedFormBlock
    )
  ) {

    const hydrated =
      sourceBlocks as FormBlock[]

    if (!groups) {
      return {
        ...schema,
        blocks: hydrated,
      }
    }

    const grouped =
      groupFieldBlocks(
        hydrated
      )

    const finalBlocks =
      groups === "tabs"
        ? buildTabs(
            grouped
          )
        : grouped

    console.log(
      "HYDRATED GROUPED",
      finalBlocks
    )

    return {
      ...schema,
      blocks: finalBlocks,
    }
  }

  /*
   * API blocks
   */

  const fieldMap =
    new Map(
      fields.map(field => [
        field.name,
        field,
      ])
    )

  const hydratedBlocks =
    sourceBlocks
      .map(block =>
        hydrateApiBlock(
          block as ApiFormBlock,
          fieldMap
        )
      )
      .filter(
        (
          block
        ): block is FormBlock =>
          Boolean(block)
      )

  const blocks =
    sourceBlocks.length > 0
      ? hydratedBlocks
      : buildBlocksFromFields(
          fields,
          groups
        )

  console.log(
    "FINAL BLOCKS",
    blocks
  )

  return {
    ...schema,
    blocks,
  }
}