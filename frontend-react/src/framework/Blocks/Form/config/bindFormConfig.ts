import type { Json } from "@/framework/types/json"
import type {
  FormConfig,
  FormEntityConfig,
} from "../types/FormConfig"

/* ============================= */
/* CONTEXT                       */
/* ============================= */

export type BindContext = {
  query?: Record<string, string | undefined>
  params?: Record<string, string | undefined>
  data?: Record<string, Json>
}

/* ============================= */
/* HELPERS                       */
/* ============================= */

// 🔥 гарантируем Json (убираем undefined)
function toJson(value: unknown): Json {
  return value === undefined ? null : (value as Json)
}

/* ============================= */
/* TOKEN RESOLVER                */
/* ============================= */

function resolveToken(
  expr: string,
  ctx: BindContext
): Json {
  const s = expr.trim()

  // =============================
  // ✅ DSL
  // =============================

  if (s.startsWith("$query.")) {
    const key = s.slice("$query.".length)
    return toJson(ctx.query?.[key])
  }

  if (s.startsWith("$params.")) {
    const key = s.slice("$params.".length)
    return toJson(ctx.params?.[key])
  }

  if (s.startsWith("$data.")) {
    const key = s.slice("$data.".length)
    return toJson(ctx.data?.[key])
  }

  // =============================
  // 🔥 FLAT ACCESS ($pair.id)
  // =============================

  if (s.startsWith("$")) {
    const path = s.slice(1).split(".")

    let current: unknown = ctx.data

    for (const key of path) {
      if (
        current === null ||
        current === undefined ||
        typeof current !== "object"
      ) {
        return null
      }

      current = (current as Record<string, unknown>)[key]
    }

    return toJson(current)
  }

  // строка без $ → как есть
  return expr
}

/* ============================= */
/* VALUE RESOLVER                */
/* ============================= */

function resolveValue(
  value: Json,
  ctx: BindContext
): Json {
  if (typeof value === "string" && value.startsWith("$")) {
    return resolveToken(value, ctx)
  }

  if (Array.isArray(value)) {
    return value.map(v =>
      resolveValue(v as Json, ctx)
    ) as Json
  }

  if (
    value &&
    typeof value === "object" &&
    !Array.isArray(value)
  ) {
    return Object.fromEntries(
      Object.entries(value).map(([k, v]) => [
        k,
        resolveValue(v as Json, ctx),
      ])
    ) as Json
  }

  return value
}

/* ============================= */
/* MAIN BIND                     */
/* ============================= */

export function bindFormConfig(
  cfg: FormConfig,
  ctx: BindContext
): FormConfig {

  const result: FormConfig = {
    ...cfg,
  }

  // =============================
  // BIND PATCH
  // =============================

  if (cfg.bind) {
    const patch: Record<string, Json> = {}

    for (const [k, v] of Object.entries(cfg.bind)) {
      if (v === undefined) continue

      patch[k] = resolveValue(v, ctx)
    }

    Object.assign(result, patch)
  }

  // =============================
  // ENTITY INITIAL
  // =============================

  if (cfg.formType === "entity") {
    const entityCfg = result as FormEntityConfig

    if (entityCfg.initial) {
      entityCfg.initial = resolveValue(
        entityCfg.initial as Json,
        ctx
      ) as Record<string, Json>
    }
  }

  return result
}