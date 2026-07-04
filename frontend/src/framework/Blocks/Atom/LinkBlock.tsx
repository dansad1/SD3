// LinkBlock.tsx

import type { ReactNode } from "react"
import { Link as RouterLink } from "react-router-dom"

import { resolveProps } from "@/framework/bind/expression/resolveProps"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"

import type { LinkBlock as TLinkBlock } from "./types"

/* ======================================================
   TYPES
   ====================================================== */

type ResolvedLinkProps = {
  label?: ReactNode

  to?: string

  external?: boolean

  newTab?: boolean

  disabled?: boolean

  icon?: ReactNode

  variant?:
    | "default"
    | "muted"
    | "subtle"
    | "danger"
    | "menu"

  underline?:
    | "always"
    | "hover"
    | "never"

  size?:
    | "sm"
    | "md"
    | "lg"
}

/* ======================================================
   SECURITY
   ====================================================== */

function isSafeExternalUrl(
  url: string,
) {
  try {
    const parsed = new URL(
      url,
      window.location.origin,
    )

    return [
      "http:",
      "https:",
      "mailto:",
    ].includes(
      parsed.protocol,
    )
  } catch {
    return false
  }
}

/* ======================================================
   COMPONENT
   ====================================================== */

export function LinkBlock({
  block,
}: {
  block: TLinkBlock
}) {
  const ctx =
    usePageRuntimeContext() as Record<
      string,
      unknown
    >

  const props = resolveProps(
    block as Record<
      string,
      unknown
    >,
    ctx,
  ) as ResolvedLinkProps

  const {
    label,

    to,

    external = false,

    newTab = false,

    disabled = false,

    icon,

    variant = "default",

    underline = "hover",

    size = "md",
  } = props

  /* ======================================================
     GUARDS
     ====================================================== */

  if (
    !to ||
    typeof to !== "string"
  ) {
    return null
  }

  /* ======================================================
     CLASSES
     ====================================================== */

  const className = [
    "ui-link",

    `variant-${variant}`,

    `underline-${underline}`,

    `size-${size}`,

    external && "external",

    disabled && "disabled",
  ]
    .filter(Boolean)
    .join(" ")

  /* ======================================================
     CONTENT
     ====================================================== */

  const content = (
    <>
      {icon && (
        <span className="ui-link-icon">
          {icon}
        </span>
      )}

      <span className="ui-link-label">
        {label}
      </span>

      {external &&
        newTab && (
          <span className="ui-link-external">
            ↗
          </span>
        )}
    </>
  )

  /* ======================================================
     DISABLED
     ====================================================== */

  if (disabled) {
    return (
      <span
        className={className}
        aria-disabled="true"
      >
        {content}
      </span>
    )
  }

  /* ======================================================
     EXTERNAL
     ====================================================== */

 if (external) {
  if (!isSafeExternalUrl(to)) {
    console.warn(
      "[Link] blocked unsafe url:",
      to,
    )

    return null
  }

  return (
    <a
      href={to}
      className={className}
      onClick={(event) => {
        event.preventDefault()

        const link =
          document.createElement("a")

        link.href = to

        document.body.appendChild(
          link,
        )

        link.click()

        document.body.removeChild(
          link,
        )
      }}
    >
      {content}
    </a>
  )
}

  /* ======================================================
     INTERNAL
     ====================================================== */

  return (
    <RouterLink
      to={to}
      className={className}
    >
      {content}
    </RouterLink>
  )
}