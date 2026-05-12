import type { ApiPageBlock } from "@/framework/page/PageSchema"
import type { BaseBlock } from "../../BlockType"

export type TabsBlock = BaseBlock & {
  type: "tabs"
  variant: "line" | "pills" | "segmented"
  align: "start" | "center" | "end"
  lazy: boolean

  blocks?: ApiPageBlock[]
}
