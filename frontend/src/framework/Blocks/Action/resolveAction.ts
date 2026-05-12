import { actionRegistry } from "./registry"

export type ResolvedAction =
  | { kind: "navigate"; to: string }
  | { kind: "backend"; code: string }
  | { kind: "ui"; id: string }
  | { kind: "page"; id: string }

export function resolveAction(
  actionId: string
): ResolvedAction {
  if (actionId.startsWith("ui.")) {
    return {
      kind: "ui",
      id: actionId,
    }
  }

  if (actionRegistry.has(actionId)) {
    return {
      kind: "ui",
      id: actionId,
    }
  }

  if (
    actionId.startsWith("form:") ||
    actionId.startsWith("action-form:")
  ) {
    return {
      kind: "page",
      id: actionId,
    }
  }

  // 🔥 сначала page navigation
  if (actionId.includes(":")) {
    return {
      kind: "navigate",
      to: actionId,
    }
  }

  // 🔥 потом backend actions
  if (
    actionId.includes(".") ||
    actionId.includes("_")
  ) {
    return {
      kind: "backend",
      code: actionId,
    }
  }

  return {
    kind: "page",
    id: actionId,
  }
}