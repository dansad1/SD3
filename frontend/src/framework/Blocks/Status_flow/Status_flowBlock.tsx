import { StatusFlowView } from "./StatusFlowView"
import type { StatusFlowBlock } from "./types"

import { useStatusFlowController } from "./useStatusFlowController"


type Props = {
  block: StatusFlowBlock
}


export function StatusFlowBlock({
  block,
}: Props) {

  const vm =
    useStatusFlowController(
      block,
    )

  return (
    <StatusFlowView
      {...vm}
    />
  )

}