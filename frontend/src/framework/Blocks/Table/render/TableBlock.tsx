import {
  CapabilityBoundary,
} from "@/framework/security/CapabilityBoundary"

import { useTableController }
  from "../controller/useTableController"

import type {
  TableApiBlock,
} from "../types/api"

import type {
  BaseRow,
} from "../types/runtime"

import { TableView }
  from "./TableView"

type Props = {
  block: TableApiBlock
}

export function TableBlock<
  T extends BaseRow
>({
  block,
}: Props) {

  const ctx =
    useTableController<T>(block)

  return (
    <CapabilityBoundary
      capabilities={ctx.capabilities}
    >
      <TableView ctx={ctx} />
    </CapabilityBoundary>
  )
}