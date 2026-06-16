import type { BlockComponent } from "../Registry/BlockRegistry"
import { MatrixBlock } from "./MatrixBlock"

export const MatrixDSLBlock: BlockComponent<"matrix"> = ({ block }) => {
  return (
    <MatrixBlock
      block={{
        code: block.source,
        params: block.params,
      }}
    />
  )
}