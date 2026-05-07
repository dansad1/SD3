import type { PageActionHandler } from "../../context/types";

export function isSameHandler(
  a: PageActionHandler,
  b: PageActionHandler
) {
  return (
    a.label === b.label &&
    a.icon === b.icon &&
    a.variant === b.variant &&
    a.order === b.order &&
    a.run === b.run &&
    a.validate === b.validate
  )
}