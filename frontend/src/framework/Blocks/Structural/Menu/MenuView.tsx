import React from "react"

type Props = {
  children?: React.ReactNode

  orientation?: "vertical" | "horizontal"

  variant?: "default" | "compact" | "cards" | "pills"

  align?: "start" | "center" | "end" | "stretch"

  gap?: "none" | "sm" | "md" | "lg"

  divided?: boolean

  wrap?: boolean
}

export function MenuView({
  children,

  orientation = "vertical",

  variant = "default",

  align = "start",

  gap = "md",

  divided = false,

  wrap = false,
}: Props) {

  const classes = [
    "ui-menu",

    `ui-menu-${orientation}`,

    `ui-menu-${variant}`,

    `ui-menu-align-${align}`,

    `ui-menu-gap-${gap}`,

    divided && "ui-menu-divided",

    wrap && "ui-menu-wrap",
  ]
    .filter(Boolean)
    .join(" ")

  return (
    <div className={classes}>
      {children}
    </div>
  )
}