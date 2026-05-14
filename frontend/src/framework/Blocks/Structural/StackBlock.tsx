// StackBlock.tsx

import type { BlockComponent } from "../Registry/BlockRegistry"

export const StackBlock: BlockComponent<"stack"> = ({
  block,
  children,
}) => {
  const className = [
    "ui-stack",

    // semantic variants
    block.variant &&
      `variant-${block.variant}`,

    // spacing
    block.gap &&
      `gap-${block.gap}`,

    // alignment
    block.align &&
      `align-${block.align}`,

    // justify
    block.justify &&
      `justify-${block.justify}`,

    // size presets
    block.size &&
      `size-${block.size}`,

    // width presets
    block.width &&
      `width-${block.width}`,

    // padding presets
    block.padding &&
      `padding-${block.padding}`,
  ]
    .filter(Boolean)
    .join(" ")

  return (
    <div className={className}>
      {children}
    </div>
  )
}