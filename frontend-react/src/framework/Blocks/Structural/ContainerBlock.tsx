// ContainerBlock.tsx

import type { BlockComponent } from "../Registry/BlockRegistry"



export const ContainerBlock: BlockComponent<"container"> = ({
  block,
  children,
}) => {
  const className = [
    "ui-container",
    block.maxWidth && `container-${block.maxWidth}`,
    block.align && `align-${block.align}`,
    block.padding && `padding-${block.padding}`,
  ]
    .filter(Boolean)
    .join(" ")

  return <div className={className}>{children}</div>
}
