// SplitBlock.tsx

import type { BlockComponent } from "../Registry/BlockRegistry"



export const SplitBlock: BlockComponent<"split"> = ({
  block,
  children,
}) => {
  return (
    <div
      className="ui-split"
      data-ratio={block.ratio ?? "1:1"}
    >
      {children}
    </div>
  )
}
