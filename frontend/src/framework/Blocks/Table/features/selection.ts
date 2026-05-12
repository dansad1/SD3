import type { BaseRow } from "../types/runtime"
import type { TableFeature } from "./types"

export function selectionFeature<T extends BaseRow>(): TableFeature<T> {
  return {
    name: "selection",
    phase: "afterList",

    apply(ctx) {
      if (!ctx.list) return ctx

      return {
        ...ctx,
        ctrl: {
          ...ctx.ctrl,
          selection: ctx.list.selection,
        },
      }
    },
  }
}

