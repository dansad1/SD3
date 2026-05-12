import { isSectionBlock, type FormBlock } from "../types/types"

export function LayoutRenderer({
  block,
  render,
}: {
  block: FormBlock
  render: (b: FormBlock) => React.ReactNode
}) {
  if (isSectionBlock(block)) {
    return (
      <div
        className="form-section form-grid"
        style={{ gridColumn: "span 12" }}
        key={block.id}
      >
        {block.title && <h3>{block.title}</h3>}

        {block.children.map(render)}
      </div>
    )
  }

  return null
}