import type { AccordionBlock } from "./types"
import { useAccordionController } from "./useAccordionController"
import { AccordionView } from "./AccordionView"

export function AccordionBlock({ block }: { block: AccordionBlock }) {
  const vm = useAccordionController(block)
  return <AccordionView {...vm} />
}
