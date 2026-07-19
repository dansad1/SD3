import type { BlockComponent } from "../Registry/BlockRegistry"

export const StackBlock: BlockComponent<"stack"> = ({
  block,
  children,
}) => {
  const className = [
    "ui-stack",

    block.variant &&
      `variant-${block.variant}`,

    block.gap &&
      `gap-${block.gap}`,

    block.align &&
      `align-${block.align}`,

    block.justify &&
      `justify-${block.justify}`,

    block.size &&
      `size-${block.size}`,

    block.width &&
      `width-${block.width}`,

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