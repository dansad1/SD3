// src/framework/Blocks/Control/types.ts


import type {
  PageBlock,
} from "@/framework/page/PageSchema"
import type { BaseBlock } from "../BlockType"

/* =========================================================
   IF
   ========================================================= */

export type IfBlock =
  BaseBlock & {

    type: "if"

    when?: string | boolean

    blocks?: PageBlock[]
  }

/* =========================================================
   FOR
   ========================================================= */

export type ForBlock =
  BaseBlock & {

    type: "for"

    each?: unknown

    range?: number | string

    as: string

    index?: string

    blocks?: PageBlock[]
  }