import { normalizeId } from "@/framework/normalize/normalizeCommon"

import type { ApiPageBlock } from "@/framework/page/PageSchema"

/* ================= TYPES ================= */

type HeadingApi = Extract<ApiPageBlock, { type: "heading" }>
type TextApi = Extract<ApiPageBlock, { type: "text" }>
type DividerApi = Extract<ApiPageBlock, { type: "divider" }>
type SpacerApi = Extract<ApiPageBlock, { type: "spacer" }>
type BadgeApi = Extract<ApiPageBlock, { type: "badge" }>
type InsertVariablesApi = Extract<
  ApiPageBlock,
  { type: "insert_variables" }
>

/* ================= NORMALIZERS ================= */

export function normalizeHeading(
  block: HeadingApi
): HeadingApi {
  return {
    ...block,
    id: normalizeId(block.id),
    level: block.level ?? 1,
    text: block.text ?? "",
  }
}

export function normalizeText(
  block: TextApi
): TextApi {
  return {
    ...block,
    id: normalizeId(block.id),
    value: block.value ?? "",
  }
}

export function normalizeDivider(
  block: DividerApi
): DividerApi {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}

export function normalizeSpacer(
  block: SpacerApi
): SpacerApi {
  return {
    ...block,
    id: normalizeId(block.id),
    size: block.size ?? 1,
  }
}

export function normalizeBadge(
  block: BadgeApi
): BadgeApi {
  return {
    ...block,
    id: normalizeId(block.id),
  }
}

export function normalizeInsertVariables(
  block: InsertVariablesApi
): InsertVariablesApi {
  return {
    ...block,
    id: normalizeId(block.id),
    title:
      block.title ??
      "Доступные переменные",
    format:
      block.format ??
      "template",
  }
}