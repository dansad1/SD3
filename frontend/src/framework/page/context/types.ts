import type { ActionContext } from "@/framework/Blocks/Action/types"
import type { PageEventHandler } from "../runtime/events/types"
import type { PageEffect } from "../runtime/effects/types"

/* ================= ACTION ================= */

export type PageActionHandler = {
  id: string

  order?: number
  label?: string
  icon?: string
  variant?: "primary" | "secondary" | "danger" | "ghost"
  placement?: "footer" | "header" | "form" | "inline"

  validate?: (ctx: ActionContext) =>
    boolean | Promise<boolean>

  run: (ctx: ActionContext) =>
    void | boolean | Promise<void | boolean>
}

export type PageRunResult =
  | "handled"
  | "not_found"
  | "failed"

/* ================= API ================= */

export type PageApi = {
  /* ACTIONS */
  registerHandler: (
    actionId: string,
    handler: PageActionHandler
  ) => void

  unregisterHandler: (
    actionId: string,
    handlerId: string
  ) => void

  run: (
    actionId: string,
    ctx?: ActionContext
  ) => Promise<PageRunResult>

  navigate: (
    to: string,
    ctx?: ActionContext
  ) => void

  /* LOADING */
  loading: {
    start: (id: string) => boolean
    finish: (id: string) => void
    isRunning: (id: string) => boolean
  }

  /* DIRTY */
  setDirty: (
    sourceId: string,
    dirty: boolean
  ) => void

  unregisterDirty: (
    sourceId: string
  ) => void

  getPageDirty: () => boolean

  /* ✅ DATA (добавить) */
  setDataKey: (
    key: string,
    value: unknown
  ) => void

  getData: () => Record<string, unknown>

  /* ✅ DSL runtime */
  setRuntimeData: (
    key: string,
    value: unknown
  ) => void

  /* EFFECTS */
  runEffect: (
    effect: PageEffect
  ) => Promise<void>

  runEffects: (
    effects?: PageEffect[] | null
  ) => Promise<void>

  /* EVENTS */
  emit: (
    event: string,
    payload?: unknown
  ) => void

  on: (
    event: string,
    handler: PageEventHandler
  ) => () => void
}
export type ActionRuntime = {
  id: string
  label: string
  handlers: PageActionHandler[]
}