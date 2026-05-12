// src/framework/BlockShell.tsx

import type { BlockLayout } from "./BlockType"




export function BlockShell({
  layout,
  children,
}: {
  layout: Required<BlockLayout>
  children: React.ReactNode
}) {
  return (
    <div
      className="page-block"
      style={{
        order: layout.order,
        gridColumn: `span ${layout.span}`,
      }}
    >
      {children}
    </div>
  )
}
