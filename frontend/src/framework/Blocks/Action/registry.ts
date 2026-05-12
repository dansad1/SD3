// src/framework/action/registry.ts

import type { ActionContext } from "./types"

export type UIActionHandler = {
  id: string
  run: (ctx: ActionContext) => boolean | Promise<boolean>
}

class ActionRegistry {
  private handlers = new Map<string, UIActionHandler>()

  register(handler: UIActionHandler) {
    this.handlers.set(handler.id, handler)
  }

  get(id: string) {
    return this.handlers.get(id)
  }

  has(id: string) {
    return this.handlers.has(id)
  }

  all() {
    return Array.from(this.handlers.values())
  }
}

export const actionRegistry = new ActionRegistry()