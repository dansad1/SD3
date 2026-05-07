import type { BaseRow } from "../types/runtime"
import type { TableFeature } from "./types"

export function searchFeature<T extends BaseRow>(): TableFeature<T> {
  return {
    name: "search",
    phase: "beforeList",

    apply(ctx) {
      if (!ctx.block.features?.search) return ctx

      return {
        ...ctx,
        listParams: {
          ...ctx.listParams,
          search: ctx.query.search || undefined,
        },
        toolbar: {
          ...ctx.toolbar,
          search: {
            value: ctx.query.search,
            onChange: ctx.query.setSearch,
          },
        },
      }
    },
  }
}

