import { usePageApi } from "@/framework/page/context/usePageApi"
import { BlockRenderer } from "../Registry/BlockRenderer"

import type { IfBlock as IfBlockType } from "./types"

import { resolvePath } from "@/framework/bind/expression/resolvePath"
import { evalExpression } from "@/framework/bind/expression/evalExpression"

function resolveCondition(
  when: unknown,
  scope: Record<string, unknown>
): boolean {
  if (typeof when === "boolean") {
    return when
  }

  if (typeof when !== "string") {
    return false
  }

  const expr = when.trim()

  if (!expr) return false

  if (expr === "true") return true
  if (expr === "false") return false

  if (expr.startsWith("${") && expr.endsWith("}")) {
    return !!evalExpression(
      expr.slice(2, -1),
      scope
    )
  }

  if (expr.startsWith("!$")) {
    return !resolvePath(
      expr.slice(2),
      scope
    )
  }

  if (expr.startsWith("$")) {
    return !!resolvePath(
      expr.slice(1),
      scope
    )
  }

  return !!expr
}

export function IfBlock({ block }: { block: IfBlockType }) {
  const page = usePageApi()
  const data = page.getData() as Record<string, unknown>

  const condition = resolveCondition(
    block.when,
    data
  )

  if (!condition) return null

  return (
  <>
    {(block.blocks ?? []).map((child, index) => (
      <BlockRenderer
        key={child.id ?? `if-child-${index}`}
        block={child}
      />
    ))}
  </>
)
}