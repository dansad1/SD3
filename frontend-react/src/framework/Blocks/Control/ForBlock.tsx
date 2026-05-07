// src/framework/Blocks/Control/ForBlock.tsx

import { Fragment } from "react"

import { BlockRenderer } from "../Registry/BlockRenderer"
import { resolvePath } from "@/framework/bind/expression/resolvePath"
import { resolveProps } from "@/framework/bind/expression/resolveProps"

import type { ForBlock as ForBlockType } from "./types"
import type {
  PageBlock,
  ApiPageBlock,
} from "@/framework/page/PageSchema"

import { usePageApi } from "@/framework/page/context/usePageApi"

/* =========================================================
   HELPERS
========================================================= */

function resolveRange(
  range: number | string | undefined,
  data: Record<string, unknown>
): number | null {

  if (typeof range === "number") return range

  if (typeof range === "string") {

    if (range.startsWith("$")) {
      const value = resolvePath(range.slice(1), data)
      if (typeof value === "number") return value
    }

    const n = Number(range)
    if (Number.isFinite(n)) return n
  }

  return null
}

/* =========================================================
   REBIND TREE
========================================================= */

function rebindTree(
  block: PageBlock,
  scope: Record<string, unknown>
): ApiPageBlock {

  const rebound = resolveProps(
    block as Record<string, unknown>,
    scope
  )

  const result: Record<string, unknown> = {
    ...block,
    ...rebound,
  }

  const blockRecord = block as Record<string, unknown>

  const nestedBlocks = blockRecord.blocks
  if (Array.isArray(nestedBlocks)) {
    result.blocks = nestedBlocks.map((child: unknown) =>
      rebindTree(
        child as PageBlock,
        scope
      )
    )
  }

  const nestedChildren = blockRecord.children
  if (Array.isArray(nestedChildren)) {
    result.children = nestedChildren.map((child: unknown) =>
      rebindTree(
        child as PageBlock,
        scope
      )
    )
  }

  return result as ApiPageBlock
}

/* =========================================================
   COMPONENT
========================================================= */

export function ForBlock({
  block,
}: {
  block: ForBlockType
}) {

  const page = usePageApi()

  const children: PageBlock[] = block.blocks ?? []

  const each = block.each
  const range = block.range
  const as = String(block.as ?? "item")
  const indexKey = block.index
    ? String(block.index)
    : undefined

  const baseData = page.getData() as Record<string, unknown>

  /* ================= RANGE ================= */

  const count = resolveRange(range, baseData)

  if (count !== null) {
    return (
      <>
        {Array.from({ length: count }).map((_, index) => {

          const childScope = {
            ...baseData,
            [as]: index,
            ...(indexKey
              ? { [indexKey]: index }
              : {}),
            $index: index,
          }

          return (
            <Fragment key={index}>
              {children.map((child, i) => {

                const reboundChild = rebindTree(
                  child,
                  childScope
                )

                return (
                  <BlockRenderer
                    key={child.id ?? `${child.type}-${i}`}
                    block={reboundChild}
                  />
                )
              })}
            </Fragment>
          )

        })}
      </>
    )
  }

  /* ================= EACH ================= */

  if (!each) return null

  let list: unknown

  if (Array.isArray(each)) {
    list = each
  } else if (
    typeof each === "string" &&
    each.startsWith("$")
  ) {
    list = resolvePath(each.slice(1), baseData)
  } else if (typeof each === "string") {
    list = baseData[each]
  } else {
    list = each
  }

  if (!Array.isArray(list)) return null

  return (
    <>
      {list.map((item, index) => {

        const childScope = {
          ...baseData,
          [as]: item,
          ...(indexKey
            ? { [indexKey]: index }
            : {}),
          $index: index,
        }

        return (
          <Fragment key={index}>
            {children.map((child, i) => {

              const reboundChild = rebindTree(
                child,
                childScope
              )

              return (
                <BlockRenderer
                  key={child.id ?? `${child.type}-${i}`}
                  block={reboundChild}
                />
              )
            })}
          </Fragment>
        )

      })}
    </>
  )
}