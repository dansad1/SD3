import type { submitAction } from "@/framework/api/action/submitAction"
import type { BaseBlock } from "../BlockType"

export type DocumentToolbar =
  | "minimal"
  | "compact"
  | "full"

export type DocumentMode =
  | "edit"
  | "read"

export type DocumentVM = {
  loading: boolean
  saving: boolean
  error: string | null

  content: string

  mode: DocumentMode
  editable: boolean
  fullscreen: boolean
  toolbar: DocumentToolbar

  setContent: (value: string) => void

  save: () => Promise<void>
}
type SubmitActionContext =
  Parameters<typeof submitAction>[2]

export type DocumentBlock = BaseBlock & {
  type: "document"

  openAction: string
  saveAction?: string

  objectId?: string

  ctx?: SubmitActionContext

  mode?: "edit" | "read"
  editable?: boolean

  autosave?: boolean
  autosaveDelay?: number

  toolbar?: "minimal" | "compact" | "full"
  fullscreen?: boolean

  refresh?: string[]
}