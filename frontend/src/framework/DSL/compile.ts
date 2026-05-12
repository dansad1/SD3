import type { DSLNode } from "./runtime"
import { Registry } from "./language"
import type { ApiPageBlock } from "../page/PageSchema"

/**
 * compileDSL
 *
 * Правила:
 * 1. DSL block type всегда хранится в поле `type`
 * 2. props не должны перезаписывать block type
 * 3. structural / control → используют `blocks`
 * 4. content → page-level блоки
 * 5. atom / action → сохраняют children
 */
export function compileDSL(node: DSLNode): ApiPageBlock[] {

  /* ===== FRAGMENT ===== */
  if (node.__dsl === "fragment") {
    return node.children.flatMap(compileDSL)
  }

  /* ===== CONTROL 🔥 НОВОЕ ===== */
  if (node.__dsl === "control") {
  const compiledChildren = node.children.flatMap(compileDSL)

  const result = {
    ...node.props,
    type: node.type,
    blocks: compiledChildren,
  }

  console.log("COMPILED CONTROL", result)

  return [result as ApiPageBlock]
}

  /* ===== BLOCK ===== */
  if (node.__dsl === "block") {
    const { __type, ...props } = node.props as {
      __type: string
      [key: string]: unknown
    }

    const compiledChildren = node.children.flatMap(compileDSL)

    /* ===== STRUCTURAL ===== */
    if (__type in Registry.structural) {
      return [
        {
          ...props,
          type: __type,
          blocks: compiledChildren,
        } as ApiPageBlock,
      ]
    }

    /* ===== DATA ===== */
    if (__type in Registry.data) {
      return [
        {
          ...props,
          type: __type,
          blocks: compiledChildren,
        } as ApiPageBlock,
      ]
    }

    /* ===== CONTENT ===== */
    if (__type in Registry.content) {
      return [
        {
          ...props,
          type: __type,
          blocks:
            compiledChildren.length > 0
              ? compiledChildren
              : undefined,
        } as ApiPageBlock,
      ]
    }

    /* ===== ATOM / ACTION ===== */
    if (__type in Registry.atom || __type in Registry.action) {
      return [
        {
          ...props,
          type: __type,
          children:
            compiledChildren.length > 0
              ? compiledChildren
              : undefined,
        } as ApiPageBlock,
      ]
    }

    throw new Error(`Unknown block type: ${__type}`)
  }

  return []
}