/* eslint-disable @typescript-eslint/no-unused-vars */

import { dsl } from "../runtime"
import type { DSLNode } from "../runtime"

export const Fragment = dsl.Fragment

export function jsx(
  type: unknown,
  props: Record<string, unknown> | null,
  _key?: unknown
): DSLNode {
  return dsl.create(type, props)
}

export const jsxs = jsx
