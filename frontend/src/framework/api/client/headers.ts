// src/framework/api/client/headers.ts
import { getCSRFToken } from "@/framework/utils/csrf"

export function buildHeaders(initial?: HeadersInit): Headers {
  const headers = new Headers(initial || {})
  const csrf = getCSRFToken()

  if (csrf) {
    headers.set("X-CSRFToken", csrf)
  }

  return headers
}