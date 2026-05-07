// StackBlock.tsx

import type { BlockComponent } from "../Registry/BlockRegistry"

export const StackBlock: BlockComponent<"stack"> = ({
  block,
  children,
}) => {
  const className = [
    "ui-stack",
    block.variant && `variant-${block.variant}`,
    block.gap && `gap-${block.gap}`,
    block.align && `align-${block.align}`,
  ]
    .filter(Boolean)
    .join(" ")

  return <div className={className}>{children}</div>
}