import type { BaseBlock } from "../../BlockType"

export type AccordionBlock = BaseBlock & {
  type: "accordion"
  multiple: any
  defaultOpen: any
}
