// framework/utils/parseApiError.ts

import type { ApiError } from "../types/ApiError"

export function parseApiError(
  e: unknown
): ApiError {
  console.log(
    "🧪 parseApiError raw",
    e
  )

  let value: unknown = e

  /*
   * Частый случай:
   * {
   *   code: "http_error",
   *   message: "{\"status\":\"error\",\"errors\":{...}}"
   * }
   */
  if (
    typeof value === "object" &&
    value !== null
  ) {
    const wrapper = value as Record<
      string,
      unknown
    >

    if (
      typeof wrapper.message === "string"
    ) {
      try {
        value = JSON.parse(
          wrapper.message
        )
      } catch {
        value = wrapper
      }
    }
  }

  /*
   * Если пришла строка JSON
   */
  if (typeof value === "string") {
    try {
      value = JSON.parse(value)
    } catch {
      return {
        code: "http_error",
        message: String(value),
      }
    }
  }

  if (
    typeof value === "object" &&
    value !== null
  ) {
    const obj = value as Record<
      string,
      unknown
    >

    const fieldErrors: Record<
      string,
      string
    > = {}

    const rawErrors =
      typeof obj.errors === "object" &&
      obj.errors !== null
        ? (obj.errors as Record<
            string,
            unknown
          >)
        : undefined

    if (rawErrors) {
      Object.entries(rawErrors).forEach(
        ([field, rawValue]) => {
          if (
            Array.isArray(rawValue) &&
            typeof rawValue[0] === "string"
          ) {
            fieldErrors[field] =
              rawValue[0]
            return
          }

          if (
            typeof rawValue === "string"
          ) {
            fieldErrors[field] =
              rawValue
          }
        }
      )
    }

    const firstFieldError =
      Object.values(fieldErrors)[0]

    return {
      code: "http_error",

      message:
        typeof obj.message === "string"
          ? obj.message
          : firstFieldError
            ? String(firstFieldError)
            : "Произошла ошибка",

      field_errors:
        Object.keys(fieldErrors).length > 0
          ? fieldErrors
          : undefined,

      details: obj,
    }
  }

  return {
    code: "network_error",
    message: "Произошла ошибка",
  }
}