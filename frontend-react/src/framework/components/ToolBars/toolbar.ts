import type { ActionContext } from "@/framework/Blocks/Action/types"

export type ToolbarAction = {
  label: string

  to?: string
  action?: string
  ctx?: ActionContext

  order?: number
  disabled?: boolean
}