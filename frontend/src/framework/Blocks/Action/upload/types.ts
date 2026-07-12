// src/framework/Blocks/Action/upload/types.ts

export type UploadPrimitive =
  | string
  | number
  | boolean


export type UploadCtx = Record<
  string,
  UploadPrimitive
>


export type UploadTempItem = {
  id: number
  name: string
  size?: number
  mime_type?: string
  url?: string
}


export type UploadResponse = {
  files: UploadTempItem[]
}


export type UploadRuntimeStatus =
  | "uploading"
  | "error"


export type UploadRuntimeItem = {
  localId: string
  name: string
  progress: number
  status: UploadRuntimeStatus
  error?: string
}


export type UploadBlock = {
  type: "upload"

  label?: string

  upload_action: string
  commit_action: string

  auto_commit?: boolean
  multiple?: boolean
  disabled?: boolean
  accept?: string

  files?: UploadTempItem[]

  ctx?: Record<string, unknown>
}