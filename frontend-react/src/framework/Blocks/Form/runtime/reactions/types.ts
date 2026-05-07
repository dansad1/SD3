import type { Json } from "@/framework/types/json"
import type { PageEffect } from "@/framework/page/runtime/effects/types"

/* =========================
   STATE
========================= */

export type FormValues = Record<string, Json>

export type FormRuntimeMeta = {
  visible: Record<string, boolean>
  disabled: Record<string, boolean>
}

export type FormRuntimeState = {
  values: FormValues
  meta: FormRuntimeMeta
}

/* =========================
   MATCH
========================= */

export type MatchRule =
  | {
      field: string
      eq?: Json
      neq?: Json
      in?: Json[]
      notIn?: Json[]
      empty?: boolean
    }
  | { all: MatchRule[] }
  | { any: MatchRule[] }
  | { not: MatchRule }

/* =========================
   EFFECTS
========================= */

export type FormEffect =
  | {
      type: "set"
      field: string
      value: Json
    }
  | {
      type: "clear"
      field: string
    }
  | {
      type: "patch"
      values: FormValues
    }
  | {
      type: "visible"
      field: string
      value: boolean
    }
  | {
      type: "disabled"
      field: string
      value: boolean
    }
  | {
      type: "fetch"
      url: string
      map: Record<string, string>
    }
  | {
      type: "page"
      effect: PageEffect
    }

/* =========================
   REACTION
========================= */

export type Reaction = {
  id?: string
  watch: string[]
  match?: MatchRule
  effects: FormEffect[]
}

/* =========================
   ENGINE TYPES
========================= */

export type RunPageEffect = (effect: PageEffect) => void