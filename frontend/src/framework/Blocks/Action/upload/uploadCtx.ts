import { resolveProps } from "@/framework/bind/expression/resolveProps"
import type { UploadCtx } from "./types"

export function resolveUploadCtx(
  raw: Record<string, unknown> | undefined,
  scope: Record<string, unknown>
): UploadCtx | undefined {
  if (!raw) return

  const resolved = resolveProps(raw, scope)

  const out: UploadCtx = {}

  for (const [k, v] of Object.entries(resolved)) {
    if (
      typeof v === "string" ||
      typeof v === "number" ||
      typeof v === "boolean"
    ) {
      out[k] = v
    }
  }

  return out
}