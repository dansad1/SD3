// src/Blocks/Action/index.ts

import { ActionBlock } from "./ActionBlock"
import { blockRegistry } from "../Registry/BlockRegistry"
import { UploadWidget } from "./upload/UploadWidget"
import type { ApiPageBlock } from "@/framework/page/PageSchema"

// ==============================
// ACTION BLOCK
// ==============================
blockRegistry.register(
  "action",
  ({ block }: { block: Extract<ApiPageBlock, { type: "action" }> }) => (
    <ActionBlock
      label={block.label}
      to={block.to}           // ✅ Navigation
      action={block.action}   // ✅ Backend / UI action
      ctx={block.ctx}         // ✅ Контекст выполнения
      variant={block.variant}
    />
  )
)

// ==============================
// UPLOAD BLOCK
// ==============================
blockRegistry.register(
  "upload",
  ({ block }) => (
    <UploadWidget block={block} />
  )
)

export {}