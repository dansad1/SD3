export type PageEventPayload = unknown

export type PageEventHandler<T = PageEventPayload> = (
  payload?: T
) => void

export type PageEventBus = {
  emit: (event: string, payload?: PageEventPayload) => void
  on: (
    event: string,
    handler: PageEventHandler
  ) => () => void
}