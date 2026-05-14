import type { PageEffect }
  from "@/framework/page/runtime/effects/types"

export interface ActionResult {
  status?: string
  message?: string
  redirect?: string
  effects?: PageEffect[]

  // 🔥 NEW
  errors?: Record<string, string[]>
}

export function isActionResult(
  value: unknown
): value is ActionResult {

  return (
    typeof value === "object" &&
    value !== null
  )
}