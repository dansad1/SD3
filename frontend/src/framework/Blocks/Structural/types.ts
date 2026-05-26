import type { PageBlock } from "@/framework/page/PageSchema"
import type { BaseBlock } from "../BlockType"

export type StructuralBlockBase = BaseBlock & {
  blocks: PageBlock[]
}

/* =====================================================
   STACK
   ===================================================== */

export type StackBlock = StructuralBlockBase & {
  type: "stack"

  gap?:
    | "none"
    | "sm"
    | "md"
    | "lg"
    | "xl"

  align?:
    | "start"
    | "center"
    | "end"
    | "stretch"

  justify?:
    | "start"
    | "center"
    | "between"
    | "end"

  variant?:
    | "default"
    | "card"

  size?:
    | "sm"
    | "md"
    | "lg"
    | "xl"
    | "full"

  width?:
    | "auto"
    | "sm"
    | "md"
    | "lg"
    | "full"

  padding?:
    | "none"
    | "sm"
    | "md"
    | "lg"
    | "xl"
}

/* =====================================================
   SECTION
   ===================================================== */

export type SectionBlock =
  StructuralBlockBase & {
    type: "section"

    title?: string
    description?: string

    variant?:
      | "default"
      | "card"

    size?:
      | "sm"
      | "md"
      | "lg"
      | "xl"

    padding?:
      | "none"
      | "sm"
      | "md"
      | "lg"
      | "xl"
  }

/* =====================================================
   SPLIT
   ===================================================== */

export type SplitBlock =
  StructuralBlockBase & {
    type: "split"

    ratio?: string

    gap?:
      | "none"
      | "sm"
      | "md"
      | "lg"
      | "xl"

    responsive?: boolean

    align?:
      | "start"
      | "center"
      | "stretch"

    collapse?:
      | "mobile"
      | "tablet"
      | "never"
  }

/* =====================================================
   CONTAINER
   ===================================================== */

export type ContainerBlock =
  StructuralBlockBase & {
    type: "container"

    maxWidth?:
      | "xs"
      | "sm"
      | "md"
      | "lg"
      | "xl"
      | "full"

    align?:
      | "left"
      | "center"
      | "right"

    padding?:
      | "none"
      | "sm"
      | "md"
      | "lg"
      | "xl"

    fluid?: boolean

    fullHeight?: boolean
  }
