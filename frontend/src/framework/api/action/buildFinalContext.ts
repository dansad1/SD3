// src/framework/api/action/buildFinalContext.ts
import type { Json } from "@/framework/types/json"

export function buildFinalContext(
  ctx?: Record<string, Json>
): Record<string, Json> {
  const urlParams = new URLSearchParams(window.location.search)
  const query = Object.fromEntries(urlParams.entries())

  return {
    ...query,       // параметры из URL
    ...(ctx ?? {}), // переданный ctx имеет приоритет
  }
}