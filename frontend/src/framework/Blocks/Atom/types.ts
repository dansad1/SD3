// src/framework/blocks/types.ts

import type { BaseBlock } from "../BlockType"


export type HeadingBlock = BaseBlock & {
  type: "heading"
  text?: string
  fallback?: string
  level?: 1 | 2 | 3 | 4
}
export type DividerBlock = BaseBlock & {
  type: "divider"
}

export type SpacerBlock = BaseBlock & {
  type: "spacer"
  size: number
}

export type TextBlock = BaseBlock & {
  type: "text"

  value?: string

  variant?:
    | "default"
    | "muted"
    | "subtle"
    | "danger"
    | "success"

  size?:
    | "sm"
    | "md"
    | "lg"
    | "xl"

  weight?:
    | "regular"
    | "medium"
    | "semibold"
    | "bold"

  align?:
    | "left"
    | "center"
    | "right"

  nowrap?: boolean
}

export type BadgeBlock = BaseBlock & {
  type: "badge"
  label: string
  color: "default" | "success" | "warning" | "danger"
  size: "sm" | "md" | "lg"
}
export type LinkBlock = BaseBlock & {
  type: "link"

  label?: string

  to?: string

  external?: boolean

  disabled?: boolean

  icon?: string

  variant?:
    | "default"
    | "muted"
    | "subtle"
    | "danger"

  underline?:
    | "always"
    | "hover"
    | "never"

  size?:
    | "sm"
    | "md"
    | "lg"
}



