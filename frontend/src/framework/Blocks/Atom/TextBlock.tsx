// TextBlock.tsx

import { resolveProps } from "@/framework/bind/expression/resolveProps"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"

import type { BlockComponent } from "../Registry/BlockRegistry"

/* ======================================================
   COMPONENT
   ====================================================== */

export const TextBlock: BlockComponent<"text"> = ({
  block,
}) => {
  const ctx =
    usePageRuntimeContext() as Record<
      string,
      unknown
    >

  const props = resolveProps(
    block as Record<string, unknown>,
    ctx
  ) as {
    value?: string

    variant?:
      | "default"
      | "muted"
      | "subtle"
      | "danger"
      | "success"

    size?:
      | "sm"
      | "md"
      | "lg"
      | "xl"

    weight?:
      | "regular"
      | "medium"
      | "semibold"
      | "bold"

    align?:
      | "left"
      | "center"
      | "right"

    nowrap?: boolean
  }

  const {
    value,

    variant = "default",

    size = "md",

    weight = "regular",

    align = "left",

    nowrap,
  } = props

  if (!value) {
    return null
  }

  const className = [
    "ui-text",

    `variant-${variant}`,

    `size-${size}`,

    `weight-${weight}`,

    `align-${align}`,

    nowrap && "nowrap",
  ]
    .filter(Boolean)
    .join(" ")

  return (
    <p className={className}>
      {value}
    </p>
  )
}