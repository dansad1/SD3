import type { Json } from "@/framework/types/json"
import type { BaseBlock } from "../../BlockType"

export type UploadTempItem = {
  id: number
  name: string
  size?: number
  url?: string
  mime?: string
}

export type UploadRefreshEffect =
  | {
      type: "entity"
      entity: string
    }
  | {
      type: "page_action"
      action: string
    }

export type UploadBlock = BaseBlock & {
  type: "upload"

  name: string
  label?: string
  multiple?: boolean

  upload_action: string
  commit_action: string

  ctx?: Record<string, unknown>

  refresh?: UploadRefreshEffect[]

  auto_commit?: boolean
  disabled?: boolean

  accept?: string

  files?: UploadTempItem[]
}
export type UploadCtx = Record<string, Json>
export type UploadResponse = {
  status: "ok"
  files: UploadTempItem[]
}