/* eslint-disable @typescript-eslint/no-unused-vars */

import type { DSLNode } from "../runtime"
import { jsx } from "./jsx-runtime"

export function jsxDEV(
  type: unknown,
  props: Record<string, unknown> | null,
  key?: unknown,
  _isStaticChildren?: boolean,
  _source?: unknown,
  _self?: unknown
): DSLNode {
  return jsx(type, props, key)
}
