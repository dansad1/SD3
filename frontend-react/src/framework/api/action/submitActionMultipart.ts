// src/framework/api/action/submitActionMultipart.ts

import { getCSRFToken } from "@/framework/utils/csrf"
import { api } from "../client"
import { buildFinalContext } from "./buildFinalContext"
import type { ActionResult, MultipartActionOptions } from "./types"
import { withTrace } from "./withTrace"

export function submitActionMultipart<T = ActionResult>(
  code: string,
  formData: FormData,
  options?: MultipartActionOptions
): Promise<T> {
  const { ctx, onProgress } = options || {}
  const finalCtx = buildFinalContext(ctx)

  formData.append("_ctx", JSON.stringify(finalCtx))

  const exec = () =>
    new Promise<T>((resolve, reject) => {
      const xhr = new XMLHttpRequest()

      xhr.open(
        "POST",
        api.buildUrl(`/action/${code}/submit/`)
      )

      xhr.withCredentials = true

      const csrf = getCSRFToken()
      if (csrf) {
        xhr.setRequestHeader("X-CSRFToken", csrf)
      }

      xhr.upload.onprogress = e => {
        if (!e.lengthComputable) return
        const percent = Math.round((e.loaded / e.total) * 100)
        onProgress?.(percent)
      }

      xhr.onload = () => {
        const contentType =
          xhr.getResponseHeader("content-type") || ""

        if (xhr.status < 200 || xhr.status >= 300) {
          reject(new Error(`HTTP ${xhr.status}`))
          return
        }

        if (!contentType.includes("application/json")) {
          reject(
            new Error(`Expected JSON, got "${contentType}"`)
          )
          return
        }

        try {
          const parsed = JSON.parse(xhr.responseText) as T
          resolve(parsed)
        } catch (e) {
          reject(
            new Error(
              e instanceof Error
                ? e.message
                : "Invalid JSON response"
            )
          )
        }
      }

      xhr.onerror = () => {
        reject(new Error("Network error"))
      }

      xhr.send(formData)
    })

  return withTrace("action_submit_multipart", exec, {
    stage: "action_submit",
    action: code,
    block: "Upload",
    multipart: true,
    hasCtx: Object.keys(finalCtx).length > 0,
  })
}