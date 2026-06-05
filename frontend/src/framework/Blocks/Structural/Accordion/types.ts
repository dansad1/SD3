import type { ReactNode } from "react"

import type {
  BaseBlock,
} from "../../BlockType"

export type AccordionItem = {
  key: string

  title: ReactNode

  content: ReactNode
}

export type AccordionBlock =
  BaseBlock & {

    type: "accordion"

    multiple?: boolean

    defaultOpen?:
      | string
      | string[]

    items: AccordionItem[]
  }

export type AccordionCtrl = {
  items: AccordionItem[]

  expanded: Set<string>

  toggle: (
    key: string
  ) => void

  multiple: boolean
}