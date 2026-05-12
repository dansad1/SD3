// src/framework/Blocks/Control/types.ts

import type { PageBlock } from "@/framework/page/PageSchema"

export type IfBlock = {
  type: "if"
  id?: string
  when?: string          // ⭐ лучше optional
  blocks?: PageBlock[]   // ⭐ лучше optional
}

// src/framework/Blocks/Control/types.ts

export type ForBlock = {
  type: "for"
  id?: string
  each?: unknown
  range?: number | string
  as: string
  index?: string
  blocks?: PageBlock[]
}