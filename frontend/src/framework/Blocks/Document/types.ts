import type { BaseBlock } from "../BlockType"

export type DocumentBlock = BaseBlock & {
  type: "document"

  /*
   * actions
   */

  openAction: string
  saveAction?: string

  /*
   * target
   */

  objectId?: string

  /*
   * runtime ctx
   */

  ctx?: Record<string, unknown>

  /*
   * editor
   */

  editable?: boolean

  autosave?: boolean
  autosaveDelay?: number

  /*
   * ui
   */

  toolbar?: (
    | "minimal"
    | "compact"
    | "full"
  )

  fullscreen?: boolean

  /*
   * integrations
   */

  refresh?: string[]
}
// types.ts

export type DocumentVM = {
  loading: boolean
  saving: boolean

  content: string

  editable: boolean
  fullscreen?: boolean

  setContent: (
    value: string
  ) => void

  save: () => void
}