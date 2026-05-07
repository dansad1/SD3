import type { FieldSchema } from "@/framework/components/dynamic/types"
import type { Json } from "@/framework/types/json"
import type { Reaction } from "../runtime/reactions/types"

/* ================= BASE ================= */

export type BaseBlock<TProps = unknown> = {
  id: string

  layout?: {
    span?: number
  }

  props?: TProps
}

export type FieldBlock = BaseBlock & {
  type: "field"
  field: FieldSchema
}

export type SectionBlock = BaseBlock & {
  type: "section"
  title?: string
  children: FormBlock[]
}

/* ================= UNION ================= */

export type FormBlock =
  | FieldBlock
  | SectionBlock

export function isSectionBlock(
  block: FormBlock
): block is SectionBlock {
  return block.type === "section"
}

/* ================= FORM SCHEMA ================= */

export type FormSchema = {
  layout?: {
    preset?: string
    override?: Record<
      string,
      {
        span?: number
      }
    >
  }

  blocks: FormBlock[]

  initial?: Record<string, Json>

  capabilities?: {
    can_edit?: boolean
  }
    reactions?: Reaction[]

}