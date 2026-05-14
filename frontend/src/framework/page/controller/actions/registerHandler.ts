
import type {
  ActionRuntime,
  PageActionHandler,
} from "../../context/types"

export function registerHandlerRuntime(
  map: Record<string, ActionRuntime>,
  actionId: string,
  handler: PageActionHandler
): boolean {

  const bucket =

    map[actionId]

    ??

    (
      map[actionId] = {

        id: actionId,

        label:
          handler.label ?? actionId,

        handlers: [],
      }
    )

  const index =
    bucket.handlers.findIndex(
      h => h.id === handler.id
    )

  /* ======================================== */
  /* NEW HANDLER */
  /* ======================================== */

  if (index < 0) {

    map[actionId] = {

      ...bucket,

      handlers: [
        ...bucket.handlers,
        handler,
      ],
    }

    return true
  }

  /* ======================================== */
  /* EXISTING */
  /* ======================================== */

  const current =
    bucket.handlers[index]

  /* ======================================== */
  /* DEDUPE */
  /* ======================================== */

  const same =

    current.run === handler.run

    &&

    current.validate ===
      handler.validate

    &&

    current.label ===
      handler.label

    &&

    current.icon ===
      handler.icon

    &&

    current.variant ===
      handler.variant

    &&

    current.order ===
      handler.order

    &&

    current.placement ===
      handler.placement

  if (same) {

    return false
  }

  /* ======================================== */
  /* UPDATE */
  /* ======================================== */

  const nextHandlers = [
    ...bucket.handlers,
  ]

  nextHandlers[index] =
    handler

  map[actionId] = {

    ...bucket,

    handlers: nextHandlers,
  }

  return true
}