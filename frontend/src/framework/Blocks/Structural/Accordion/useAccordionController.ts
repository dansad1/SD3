import { useState } from "react"

import type {
  AccordionBlock,
  AccordionCtrl,
} from "./types"

export function useAccordionController(
  block: AccordionBlock
): AccordionCtrl {

  const multiple =
    block.multiple ?? false

  const defaultOpen =
    Array.isArray(
      block.defaultOpen
    )
      ? block.defaultOpen
      : block.defaultOpen
        ? [block.defaultOpen]
        : []

  const [
    expanded,
    setExpanded,
  ] = useState(
    () => new Set(defaultOpen)
  )

  const toggle = (
    key: string
  ) => {

    setExpanded(
      current => {

        const next =
          new Set(current)

        if (
          next.has(key)
        ) {

          next.delete(key)

          return next
        }

        if (
          !multiple
        ) {

          next.clear()
        }

        next.add(key)

        return next
      }
    )
  }

  return {
    items:
      block.items,

    expanded,

    toggle,

    multiple,
  }
}