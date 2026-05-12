import type { BlockComponent } from "../../Registry/BlockRegistry"
import { useResourceController } from "../controller/useResourceController"

export const ResourceBlockComponent: BlockComponent<"resource"> = ({
  block,
  children,
}) => {
  const { loading } = useResourceController(block)

  return (
    <>
      {loading && <div>Loading...</div>}
      {children}
    </>
  )
}