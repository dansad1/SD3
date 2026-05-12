import type { BlockComponent } from "../Registry/BlockRegistry"

export const TextBlock: BlockComponent<"text"> = ({ block }) => {
  return (
    <p className={block.muted ? "text-muted" : undefined}>
      {block.value}
    </p>
  )
}
