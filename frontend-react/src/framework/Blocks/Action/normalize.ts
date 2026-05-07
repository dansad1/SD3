import { normalizeId } from "@/framework/normalize/normalizeCommon"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

type ActionApi = Extract<ApiPageBlock, { type: "action" }>

export function normalizeAction(
  block: ActionApi
): ActionApi {
  if ("run" in (block as Record<string, unknown>)) {
    console.error("Action DSL: 'run' больше не поддерживается", block)
  }

  const to = block.to
  const action = block.action

  if (to && action) {
    console.warn(
      "ActionBlock: both 'to' and 'action' provided, 'to' will be used",
      block
    )
  }

  return {
    ...block,
    id: normalizeId(block.id),
    to,
    action,
  }
}

/* ================= NORMALIZER ================= */


