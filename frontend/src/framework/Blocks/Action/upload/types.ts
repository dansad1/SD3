import type { Json } from "@/framework/types/json"

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

export type UploadBlock = {
  type: "upload"
  id?: string
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