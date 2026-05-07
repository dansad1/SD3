// src/framework/api/client/errorUtils.ts

import type { ApiError } from "@/framework/types/ApiError";

export function getErrorMessage(e: unknown): string {
  if (e instanceof Error) return e.message

  if (typeof e === "object" && e !== null && "message" in e) {
    const msg = (e as { message?: unknown }).message
    if (typeof msg === "string") return msg
  }

  return String(e)
}

export function normalizeApiErrorMessage(
  status: number,
  contentType: string,
  body: string
): { short: string; details?: string } {
  if (contentType.includes("text/html")) {
    const title = body.match(/<title>(.*?)<\/title>/i)?.[1]
    const h1 = body.match(/<h1>(.*?)<\/h1>/i)?.[1]

    return {
      short:
        title?.trim() ||
        h1?.trim() ||
        `HTTP ${status} HTML error`,
      details: body.slice(0, 1500),
    }
  }

  if (body.length > 400) {
    return {
      short: body.slice(0, 200) + "...",
      details: body,
    }
  }

  return {
    short: body || `HTTP ${status}`,
  }
}

export function createApiError(
  status: number,
  contentType: string,
  body: string
): ApiError {
  const norm = normalizeApiErrorMessage(
    status,
    contentType,
    body
  )

  return {
    code: "http_error",
    message: norm.short,
    details: norm.details,
    status,
  }
}