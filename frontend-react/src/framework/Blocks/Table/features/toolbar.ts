// src/framework/Blocks/Table/features/toolbar.ts

import type { TableFeature } from "./types"
import type { BaseRow } from "../types/runtime"
import type { ToolbarAction } from "@/framework/components/ToolBars/toolbar"

const DEFAULT_ACTION_MAP: Record<string, string> = {
  reload: "ui.reloadTable",
  fields: "ui.openFields",
}

export function toolbarFeature<T extends BaseRow>(): TableFeature<T> {
  return {
    name: "toolbar",
    phase: "afterList",

    apply(ctx) {
      const actions = ctx.block.toolbar?.actions
      if (!actions || !ctx.list) return ctx

      const mapped: ToolbarAction[] = actions.map((a) => {
        // shorthand: "reload"
        if (typeof a === "string") {
          return {
            label: a,
            action: DEFAULT_ACTION_MAP[a] ?? a,
            ctx: {
              entity: ctx.entity,
              list: ctx.list,
              modals: ctx.modals,
            },
          }
        }

        // object DSL
        return {
          label: a.label ?? "",
          to: a.to,
          action: a.action,
          ctx: {
            entity: ctx.entity,
            list: ctx.list,
            modals: ctx.modals,
            ...(a.ctx || {}),
          },
          order: a.order,
          disabled: a.disabled,
        }
      })

      return {
        ...ctx,
        toolbar: {
          ...ctx.toolbar,
          actions: mapped,
        },
      }
    },
  }
}