import type { BlockComponent }
  from "../../Registry/BlockRegistry"

export const MenuBlock:
  BlockComponent<"menu"> = ({
    block,
    children,
  }) => {

  const classes = [

    "ui-menu",

    `ui-menu-${block.orientation ?? "vertical"}`,

    `ui-menu-${block.variant ?? "default"}`,

    `ui-menu-align-${block.align ?? "start"}`,

    `ui-menu-gap-${block.gap ?? "md"}`,

    block.divided &&
      "ui-menu-divided",

    block.wrap &&
      "ui-menu-wrap",

  ]
    .filter(Boolean)
    .join(" ")

  return (
    <nav className={classes}>
      {children}
    </nav>
  )
}