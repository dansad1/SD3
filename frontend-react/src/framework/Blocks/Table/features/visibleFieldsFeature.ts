// src/framework/Blocks/Table/features/visibleFieldsFeature.ts

import type { TableFeature } from "./types"
import type { BaseRow } from "../types/runtime"

function createModalController() {
  let isOpen = false

  return {
    get isOpen() {
      return isOpen
    },
    open() {
      isOpen = true
    },
    close() {
      isOpen = false
    },
  }
}

export function visibleFieldsFeature<T extends BaseRow>(): TableFeature<T> {
  return {
    name: "visibleFields",
    phase: "afterList",

    apply(ctx) {
      return {
        ...ctx,
        modals: {
          ...ctx.modals,
          visibleFields:
            ctx.modals?.visibleFields ?? createModalController(),
        },
      }
    },
  }
}