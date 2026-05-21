import { actionRegistry }
  from "./registry"

export type ResolvedAction =

  | {
      kind: "navigate"
      to: string
    }
  | {

      kind: "backend"
      code: string
      target?: string
    }

  | {

      kind: "ui"

      id: string
    }

  | {

      kind: "page"

      id: string
    }

type ResolveInput = {

  action?: string

  target?: string

  to?: string
}

export function resolveAction(
  input: ResolveInput
): ResolvedAction {

  /* ==================================================== */
  /* NAVIGATION */
  /* ==================================================== */

  if (input.to) {

    return {

      kind: "navigate",

      to: input.to,
    }
  }

  const actionId =
    input.action

  if (!actionId) {

    return {

      kind: "page",

      id: "",
    }
  }

  /* ==================================================== */
  /* UI */
  /* ==================================================== */

  if (
    actionId.startsWith("ui.")
  ) {

    return {

      kind: "ui",

      id: actionId,
    }
  }

  if (
    actionRegistry.has(actionId)
  ) {

    return {
      kind: "ui",
      id: actionId,
    }
  }
  /* ==================================================== */
  /* PAGE */
  /* ==================================================== */
  if (

    actionId.startsWith("form:") ||
    actionId.startsWith(
      "action-form:"
    )
  ) {

    return {
      kind: "page",
      id: actionId,
    }
  }

  /* ==================================================== */
  /* ROUTE NAVIGATION */
  /* ==================================================== */

  if (
    actionId.includes(":")
  ) {

    return {

      kind: "navigate",

      to: actionId,
    }
  }

  /* ==================================================== */
  /* BACKEND */
  /* ==================================================== */

  if (

    actionId.includes(".") ||

    actionId.includes("_")

  ) {

    return {

      kind: "backend",

      code: actionId,

      target:
        input.target,
    }
  }

  /* ==================================================== */
  /* FALLBACK */
  /* ==================================================== */

  return {

    kind: "page",

    id: actionId,
  }
}