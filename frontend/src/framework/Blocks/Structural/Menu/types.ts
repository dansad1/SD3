
import type { BaseBlock }
  from "../../BlockType"

export type MenuBlock =
  BaseBlock & {

    type: "menu"

    children?: unknown[]

    orientation?:
      | "vertical"
      | "horizontal"

    variant?:
      | "default"
      | "compact"
      | "cards"
      | "pills"

    align?:
      | "start"
      | "center"
      | "end"
      | "stretch"

    gap?:
      | "none"
      | "sm"
      | "md"
      | "lg"

    divided?: boolean

    wrap?: boolean
  }