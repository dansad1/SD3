import type { DSLNode } from "../runtime"
import type { DSLChildren, DSLChild } from "./types"

/**
 * Нормализация children:
 * - всегда массив
 * - убираем null / undefined / false
 */
export function normalizeChildren(
  children?: DSLChildren
): DSLNode[] {
  if (!children) return []

  const arr: DSLChild[] = Array.isArray(children)
    ? children
    : [children]

  return arr.filter(
    (c): c is DSLNode =>
      c !== null &&
      c !== undefined &&
      c !== false
  )
}