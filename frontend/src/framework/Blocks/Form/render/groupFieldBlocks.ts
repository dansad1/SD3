import type {
  FormBlock,
} from "../types/types"

import type {
  FieldSchema,
} from "@/framework/components/dynamic/types"

type SectionMeta = {
  key: string
  title?: string
}

function normalizeSection(
  field: FieldSchema
): SectionMeta | null {

  const raw =
    field.ui?.section

  if (!raw) {
    return null
  }

  if (typeof raw === "string") {
    return {
      key: raw,
      title: raw,
    }
  }

  return {
    key: raw.key,
    title:
      raw.title ??
      raw.key,
  }
}

function fieldBlock(
  field: FieldSchema
): FormBlock {

  return {
    id:
      `field.${field.name}`,

    type: "field",

    field,
  }
}

export function buildTabs(
  blocks: FormBlock[]
): FormBlock[] {

  console.log(
    "🔥 BUILD TABS INPUT",
    blocks
  )

  const sections =
    blocks.filter(
      block =>
        block.type ===
        "section"
    )

  console.log(
    "🔥 BUILD TABS SECTIONS",
    sections
  )

  if (
    sections.length <= 1
  ) {

    console.warn(
      "🔥 NOT ENOUGH SECTIONS FOR TABS"
    )

    return blocks
  }

  const result: FormBlock[] = [
    {
      id: "tabs",

      type: "tabs",

      variant: "line",

      children: sections,
    },
  ]

  console.log(
    "🔥 BUILD TABS RESULT",
    result
  )

  return result
}

export function groupFieldBlocks(
  blocks: FormBlock[]
): FormBlock[] {

  const ungrouped: FormBlock[] = []

  const groups = new Map<
    string,
    {
      meta: SectionMeta
      blocks: FormBlock[]
    }
  >()

  for (const block of blocks) {

    if (
      block.type !== "field"
    ) {
      ungrouped.push(block)
      continue
    }

    const section =
      normalizeSection(
        block.field
      )

    if (!section) {
      ungrouped.push(block)
      continue
    }

    if (
      !groups.has(
        section.key
      )
    ) {
      groups.set(
        section.key,
        {
          meta: section,
          blocks: [],
        }
      )
    }

    groups
      .get(section.key)!
      .blocks
      .push(block)
  }

  const result: FormBlock[] = []

  if (ungrouped.length) {
    result.push({
      id: "section.main",
      type: "section",
      title: "Основное",
      children: ungrouped,
    })
  }

  for (const group of groups.values()) {
    result.push({
      id:
        `section.${group.meta.key}`,
      type: "section",
      title:
        group.meta.title,
      children:
        group.blocks,
    })
  }

  return result
}

export function buildBlocksFromFields(
  fields: FieldSchema[],
  groups?:
    | "sections"
    | "tabs"
): FormBlock[] {

  console.log(
    "🔥 GROUP MODE",
    groups
  )

  console.table(
    fields.map(field => ({
      name:
        field.name,

      section:
        field.ui?.section,
    }))
  )

  if (!groups) {

    console.warn(
      "🔥 NO GROUP MODE"
    )

    return fields.map(
      fieldBlock
    )
  }

  const grouped =
    groupFieldBlocks(
      fields.map(
        fieldBlock
      )
    )

  console.log(
    "🔥 GROUPED BLOCKS",
    grouped
  )

  if (groups === "tabs") {

    const tabs =
      buildTabs(
        grouped
      )

    console.log(
      "🔥 FINAL TABS",
      tabs
    )

    return tabs
  }

  return grouped
}