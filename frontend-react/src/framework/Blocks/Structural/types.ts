import type { PageBlock } from "@/framework/page/PageSchema"
import type { BaseBlock } from "../BlockType"

export type StructuralBlockBase = BaseBlock & {
  blocks: PageBlock[]
}
export type StackBlock = StructuralBlockBase & {
  type: "stack"
  gap?: "none" | "sm" | "md" | "lg"
  align?: "start" | "center" | "end" | "stretch"
  variant?: "default" | "card"
}

export type SectionBlock = StructuralBlockBase & {
  type: "section"
  title?: string
  description?: string
}

export type SplitBlock = StructuralBlockBase & {
  type: "split"
  ratio?: string
  gap?: "none" | "sm" | "md" | "lg"
  responsive?: boolean
}

export type ContainerBlock = StructuralBlockBase & {
  type: "container"
  maxWidth?: "xs" | "sm" | "md" | "lg" | "xl"
  align?: "left" | "center" | "right"
  padding?: "none" | "sm" | "md" | "lg"
}

