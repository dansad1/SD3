// LinkBlock.tsx

import { Link as RouterLink } from "react-router-dom"
import type { ReactNode } from "react"

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
  disabled?: boolean

  icon?: ReactNode

  variant?:
    | "default"
    | "muted"
    | "subtle"
    | "danger"

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

function isSafeExternalUrl(url: string) {
  return (
    url.startsWith("http://") ||
    url.startsWith("https://") ||
    url.startsWith("mailto:")
  )
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
    block as Record<string, unknown>,
    ctx
  ) as ResolvedLinkProps

  const {
    label,
    to,

    external,
    disabled,

    icon,

    variant = "default",

    underline = "hover",

    size = "md",
  } = props

  /* ======================================================
     GUARDS
     ====================================================== */

  if (!to || typeof to !== "string") {
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

      {external && (
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
        to
      )

      return null
    }

    return (
      <a
        href={to}
        target="_blank"
        rel="noopener noreferrer"
        className={className}
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