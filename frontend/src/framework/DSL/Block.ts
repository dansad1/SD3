import type { DSLNode } from "./runtime"

export function Block(
  props: Record<string, unknown>,
  children: DSLNode[]
): DSLNode {
  return {
    __dsl: "block",
    props,
    children,
  }
}
