// src/framework/DSL/page.ts

import type { DSLNode } from "./runtime"
import { compileDSL } from "./compile"
import type { ApiPageSchema } from "../page/PageSchema"

export function page(
  id: string,
  root: DSLNode
): ApiPageSchema {

  const blocks = compileDSL(root)


  return {
    id,
    blocks,
  }
}

