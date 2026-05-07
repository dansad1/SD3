import type { PageEffect } from "@/framework/page/runtime/effects/types"

export function isActionResult(
  value: unknown
): value is {
  status?: string
  message?: string
  redirect?: string
  effects?: PageEffect[]
} {
  return (
    typeof value === "object" &&
    value !== null
  )
}