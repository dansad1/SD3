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


export type UploadActionErrorMap = Record<
  string,
  string[] | string
>


export type UploadActionResult = {
  status?: "ok" | "error"
  errors?: UploadActionErrorMap
  [key: string]: unknown
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


export type StoredFile = {
  id: number
  name: string
  size: number
  mime_type: string
  url: string
}


export type UploadBlock = {
  type: "upload"
  id?: string

  name?: string
  label?: string

  upload_action: string
  commit_action?: string
  discard_action?: string

  /*
   * Если задано, контроллер возьмёт массив файлов
   * из result[result_key].
   *
   * Для files.upload:
   * result_key="files"
   *
   * Для произвольного multipart action
   * можно не задавать.
   */
  result_key?: string

  auto_commit?: boolean
  multiple?: boolean
  disabled?: boolean
  accept?: string

  files?: UploadTempItem[]

  ctx?: Record<string, unknown>
  refresh?: unknown[]
}