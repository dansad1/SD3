// src/framework/api/action/types.ts
import type { PageEffect } from "@/framework/page/runtime/effects/types"
import type { Json } from "@/framework/types/json"

export type ActionResult = {
  status: "ok" | "error" | "accepted"
  message?: string
  errors?: Record<string, string[]>
  effects?: PageEffect[]
  redirect?: string
  [key: string]: unknown
}

export type MultipartActionOptions = {
  ctx?: Record<string, Json>
  onProgress?: (percent: number) => void
}