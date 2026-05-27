import { resolveProps } from "@/framework/bind/expression/resolveProps"

import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"

import type { MenuBlock } from "./types"

export function useMenuController(
  block: MenuBlock
) {

  const ctx =
    usePageRuntimeContext() as Record<
      string,
      unknown
    >

  return resolveProps(
    block as Record<string, unknown>,
    ctx
  )
}