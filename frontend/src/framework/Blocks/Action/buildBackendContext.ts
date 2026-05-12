import type { ActionContext } from "./types"
import type { Json } from "@/framework/types/json"

function isPrimitive(value: unknown): value is Json {
  return (
    value === null ||
    typeof value === "string" ||
    typeof value === "number" ||
    typeof value === "boolean"
  )
}

function isJsonObject(value: unknown): value is Record<string, Json> {
  return (
    typeof value === "object" &&
    value !== null &&
    !Array.isArray(value)
  )
}

export function buildBackendContext(
  ctx: ActionContext
): Record<string, Json> {
  const result: Record<string, Json> = {}

  for (const [key, value] of Object.entries(ctx)) {
    if (isPrimitive(value)) {
      result[key] = value
      continue
    }

    // row нужно сохранять целиком
    if (key === "row" && isJsonObject(value)) {
      result[key] = value
      continue
    }
  }

  const query = ctx.page?.query

  if (query) {
    for (const [key, value] of Object.entries(query)) {
      if (isPrimitive(value) && !(key in result)) {
        result[key] = value
      }
    }
  }

  console.log(
    "🧩 BUILD BACKEND CONTEXT JSON",
    JSON.stringify(
      {
        input: ctx,
        output: result,
      },
      null,
      2
    )
  )

  return result
}