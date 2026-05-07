import type { ApiPageBlock } from "@/framework/page/PageSchema"
import { resolvePath } from "@/framework/bind/expression/resolvePath"
import { resolveProps } from "@/framework/bind/expression/resolveProps"

type BlockWithChildren = ApiPageBlock & {
  blocks?: ApiPageBlock[]
  children?: ApiPageBlock[]
  each?: unknown
  as?: string
  index?: string
  title?: string
  when?: unknown
  type?: string
}

/* =========================
   REBIND TREE
========================= */

export function rebindTree(
  block: ApiPageBlock,
  scope: Record<string, unknown>
): ApiPageBlock {
  const rebound = resolveProps(
    block as Record<string, unknown>,
    scope
  )

  const result: Record<string, unknown> = {
    ...block,
    ...rebound,
  }

  const blockRecord = block as Record<string, unknown>

  if (Array.isArray(blockRecord.blocks)) {
    result.blocks = blockRecord.blocks.map(child =>
      rebindTree(child as ApiPageBlock, scope)
    )
  }

  if (Array.isArray(blockRecord.children)) {
    result.children = blockRecord.children.map(child =>
      rebindTree(child as ApiPageBlock, scope)
    )
  }

  return result as ApiPageBlock
}

/* =========================
   CONDITION
========================= */

export function resolveCondition(
  when: unknown,
  scope: Record<string, unknown>
): boolean {
  if (typeof when === "boolean") return when
  if (typeof when !== "string") return false

  const expr = when.trim()

  if (!expr) return false
  if (expr === "true") return true
  if (expr === "false") return false

  if (expr.startsWith("!$")) {
    return !resolvePath(expr.slice(2), scope)
  }

  if (expr.startsWith("$")) {
    return !!resolvePath(expr.slice(1), scope)
  }

  return !!expr
}

/* =========================
   BUILD TABS
========================= */

export function buildTabs(
  blocks: ApiPageBlock[] | undefined,
  baseData: Record<string, unknown>
): ApiPageBlock[] {
  if (!blocks) return []

  const visible = blocks.flatMap(item => {
    const b = item as BlockWithChildren

    if (b.type === "if") {
      return resolveCondition(b.when, baseData)
        ? b.blocks ?? []
        : []
    }

    return [item]
  })

  return visible.flatMap(tab => {
    const t = tab as BlockWithChildren

    if (t.type !== "for") {
      return [tab]
    }

    let list: unknown = t.each

    if (typeof list === "string" && list.startsWith("$")) {
      list = resolvePath(list.slice(1), baseData)
    }

    if (!Array.isArray(list)) return []

    const asKey =
      typeof t.as === "string" && t.as.length > 0
        ? t.as
        : "item"

    return list.map((item, index) => {
      const scope: Record<string, unknown> = {
        ...baseData,
        [asKey]: item,
        ...(t.index ? { [t.index]: index } : {}),
        $index: index,
      }

      const titleValue =
        typeof t.title === "string"
          ? resolveProps({ title: t.title }, scope).title
          : resolveProps(
              { title: `$${asKey}.discipline` },
              scope
            ).title

      const title =
        typeof titleValue === "string"
          ? titleValue
          : String(titleValue ?? `Tab ${index + 1}`)

      const rebound = rebindTree(
        {
          ...t,
          blocks: t.blocks ?? [],
        } as ApiPageBlock,
        scope
      )

      return {
        ...rebound,
        title,
      } as ApiPageBlock
    })
  })
}