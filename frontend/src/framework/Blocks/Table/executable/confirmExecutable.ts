// table/runtime/executable/confirmExecutable.ts

import type { ExecutableAction } from "./types"

export function confirmExecutable(
  action: ExecutableAction
) {
  if (!action.confirm) {
    return true
  }

  const message =
    typeof action.confirm === "object"
      ? action.confirm.message ||
        "Выполнить действие?"
      : "Выполнить действие?"

  return window.confirm(message)
}