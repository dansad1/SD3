import {
  StatusFlowView,
} from "./StatusFlowView"

import {
  useStatusFlowController,
} from "./useStatusFlowController"

import type {
  StatusFlowBlock as StatusFlowBlockType,
} from "./types"


type Props = {
  block: StatusFlowBlockType
}


export function StatusFlowBlock({
  block,
}: Props) {
  const viewModel =
    useStatusFlowController(
      block,
    )

  return (
    <StatusFlowView
      {...viewModel}
    />
  )
}