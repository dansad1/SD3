import type { PageActionsBlockType } from "./types"


export function PageActionsBlock({
  block,
  children,
}: {
  block: PageActionsBlockType

  children?: React.ReactNode
}) {

  const className = [

    "page-actions",

    block.sticky
      ? "page-actions-sticky"
      : "",

    block.align
      ? `page-actions-${block.align}`
      : "",

  ]
    .filter(Boolean)
    .join(" ")

  return (

    <div className={className}>

      {children}

    </div>
  )
}