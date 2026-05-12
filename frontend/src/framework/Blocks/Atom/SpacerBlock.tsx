import type { BlockComponent } from "../Registry/BlockRegistry"

export const SpacerBlock: BlockComponent<"spacer"> = ({ block }) => {
  return <div style={{ height: block.size ?? 0 }} />
}
