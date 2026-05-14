// ContainerBlock.tsx

import type { BlockComponent } from "../Registry/BlockRegistry"

export const ContainerBlock: BlockComponent<"container"> = ({
  block,
  children,
}) => {
  const className = [
    "ui-container",

    // max width
    block.maxWidth &&
      `container-${block.maxWidth}`,

    // alignment
    block.align &&
      `align-${block.align}`,

    // padding
    block.padding &&
      `padding-${block.padding}`,

    // fluid mode
    block.fluid &&
      "fluid",

    // full height
    block.fullHeight &&
      "full-height",
  ]
    .filter(Boolean)
    .join(" ")

  return (
    <div className={className}>
      {children}
    </div>
  )
}