// InsertVariablesBlock/types.ts

import type { BaseBlock } from "../../BlockType"

/* ================= DATA ================= */

export type InsertVariableItem = {
  key: string
  label: string
  value: string
}

export type InsertVariableGroup = {
  key: string
  label: string
  items: InsertVariableItem[]
}

/* ================= BACKEND RESPONSE ================= */

export type InsertVariablesResponse = {
  title?: string
  groups: InsertVariableGroup[]
  onInsert?: {
    type: string
    payload?: Record<string, unknown>
  }
}

/* ================= BLOCK ================= */

export type InsertVariablesBlockType = BaseBlock & {
  type: "insert_variables"
  source: string

  targetField: string // ✅ ВОТ ЭТО НУЖНО

  title?: string
  format?: "template" | "raw" | "dollar"
}