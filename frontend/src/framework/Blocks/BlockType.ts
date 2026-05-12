// src/framework/blocks/base.ts


export type BaseBlock = {
  id?: string | number
  layout?: BlockLayout
}
// src/framework/blocks/layout.ts

export type LayoutSpan = 1 | 2 | 3 | 4 | 6 | 12

export type Area =
  | "main"
  | "sidebar-left"
  | "sidebar-right"
  | "overlay"

export type BlockLayout = {
  order?: number
  span?: LayoutSpan
  hidden?: boolean
  area?: Area
}