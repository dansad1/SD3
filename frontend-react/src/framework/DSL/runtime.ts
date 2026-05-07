/* ===================== KINDS ===================== */

export type ContentKind =
  | "form"
  | "table"
  | "matrix"
  | "heading"
  | "divider"
  | "spacer"

/* ===================== NODES ===================== */

export type DSLNode =
  | BlockNode
  | ControlNode   // 🔥 НОВОЕ
  | ContentNode
  | FragmentNode

export type BlockNode = {
  __dsl: "block"
  props: unknown
  children: DSLNode[]
}

/* 🔥 CONTROL NODE */

export type ControlNode = {
  __dsl: "control"
  type: string
  props: Record<string, unknown>
  children: DSLNode[]
}

export type ContentNode = {
  __dsl: "content"
  kind: ContentKind
  props: unknown
}

export type FragmentNode = {
  __dsl: "fragment"
  children: DSLNode[]
}

/* ===================== JSX RUNTIME ===================== */

export const dsl = {
  create(type: unknown, props: unknown, ...children: unknown[]): DSLNode {
    /* ===== FRAGMENT ===== */
    if (type === dsl.Fragment) {
      return {
        __dsl: "fragment",
        children: normalize(children),
      }
    }

    /* ===== FUNCTION COMPONENT ===== */
    if (typeof type === "function") {
      return type(props ?? {}, normalize(children))
    }

    /* ===== CONTENT (string) ===== */
    if (typeof type === "string") {
      return {
        __dsl: "content",
        kind: type as ContentKind,
        props,
      }
    }

    throw new Error("Unsupported DSL node")
  },

  Fragment(_: unknown, children: unknown[]): FragmentNode {
    return {
      __dsl: "fragment",
      children: normalize(children),
    }
  },
}

/* ===================== EXPORTS FOR JSX ===================== */

export { dsl as jsx, dsl as jsxs, dsl as Fragment }

/* ===================== HELPERS ===================== */

function normalize(input: unknown[]): DSLNode[] {
  return input.flatMap((child) => {
    if (Array.isArray(child)) return normalize(child)
    if (isDSLNode(child)) return [child]
    return []
  })
}

function isDSLNode(x: unknown): x is DSLNode {
  return typeof x === "object" && x !== null && "__dsl" in x
}