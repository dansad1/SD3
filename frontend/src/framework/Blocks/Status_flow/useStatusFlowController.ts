import {
  resolveProps,
} from "@/framework/bind/expression/resolveProps"

import type {
  BindScope,
} from "@/framework/bind/types"

import {
  usePageRuntimeContext,
} from "@/framework/page/runtime/usePageRuntimeContext"

import {
  useStatusFlow,
} from "./useStatusFlow"

import type {
  StatusFlowBlock,
  StatusFlowVM,
} from "./types"


export function useStatusFlowController(
  block: StatusFlowBlock,
): StatusFlowVM {
  const runtime =
    usePageRuntimeContext()

  const props =
    resolveProps(
      block as Record<
        string,
        unknown
      >,
      runtime as unknown as BindScope,
    ) as StatusFlowBlock

  return useStatusFlow(
    props.source,
    props.editable === true,
  )
}