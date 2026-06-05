import { AccordionView }
  from "./AccordionView"

import type {
  AccordionBlock,
} from "./types"

import {
  useAccordionController,
} from "./useAccordionController"

export function AccordionBlock({
  block,
}: {
  block: AccordionBlock
}) {

  const ctrl =
    useAccordionController(
      block
    )

  return (
    <AccordionView
      ctrl={ctrl}
    />
  )
}