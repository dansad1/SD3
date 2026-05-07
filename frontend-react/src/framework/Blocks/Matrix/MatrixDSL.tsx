// MatrixDSLBlock.tsx
import type { BlockComponent } from "../Registry/BlockRegistry"
import { MatrixBlock } from "./MatrixBlock"

export const MatrixDSLBlock: BlockComponent<"matrix"> = ({ block }) => {
  return (
    <MatrixBlock
      code={block.source}     // 🔥 было block.code → ошибка
      context={block.params}  // 🔥 было block.context
    />
  )
}