import type { BaseBlock } from "../BlockType"

export type CustomBlock = BaseBlock & {
  type: "custom"
  component: any
  props: any
}
