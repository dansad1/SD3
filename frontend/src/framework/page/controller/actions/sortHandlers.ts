import type { PageActionHandler } from "../../context/types";

export function sortHandlers(handlers: PageActionHandler[]) {
  return [...handlers].sort(
    (a, b) => (a.order ?? 0) - (b.order ?? 0)
  )
}