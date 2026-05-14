// framework/utils/parseApiError.ts

import type { ApiError }
  from "../types/ApiError"

export function parseApiError(
  e: unknown
): ApiError {

  console.log(
    "🧪 parseApiError raw",
    e
  )

  let value: unknown = e

  // =====================================================
  // WRAPPER JSON
  // =====================================================

  if (
    typeof value === "object" &&
    value !== null
  ) {

    const wrapper =
      value as Record<
        string,
        unknown
      >

    if (
      typeof wrapper.message ===
      "string"
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

  // =====================================================
  // STRING JSON
  // =====================================================

  if (
    typeof value === "string"
  ) {

    try {

      value = JSON.parse(value)

    } catch {

      return {
        code: "http_error",
        message: String(value),
      }
    }
  }

  // =====================================================
  // OBJECT
  // =====================================================

  if (
    typeof value === "object" &&
    value !== null
  ) {

    const obj =
      value as Record<
        string,
        unknown
      >

    // ===================================================
    // FIELD ERRORS
    // ===================================================

    const fieldErrors:
      Record<
        string,
        string[]
      > = {}

    // backend:
    // errors
    // field_errors

    const rawErrors =
      typeof obj.field_errors ===
        "object" &&
      obj.field_errors !== null

        ? obj.field_errors as Record<
            string,
            unknown
          >

        : typeof obj.errors ===
            "object" &&
          obj.errors !== null

          ? obj.errors as Record<
              string,
              unknown
            >

          : undefined

    if (rawErrors) {

      Object.entries(rawErrors)
        .forEach(
          (
            [field, rawValue]
          ) => {

            if (
              Array.isArray(rawValue)
            ) {

              fieldErrors[field] =
                rawValue
                  .filter(
                    v =>
                      typeof v ===
                      "string"
                  )

              return
            }

            if (
              typeof rawValue ===
              "string"
            ) {

              fieldErrors[field] = [
                rawValue,
              ]
            }
          }
        )
    }

    // ===================================================
    // FIRST FIELD ERROR
    // ===================================================

    const firstFieldError =

      Object.values(
        fieldErrors
      )[0]?.[0]

    // ===================================================
    // MESSAGE
    // ===================================================

    let message =
      "Произошла ошибка"

    // validation priority

    if (firstFieldError) {

      message =
        firstFieldError

    } else if (
      typeof obj.message ===
      "string"
    ) {

      message =
        obj.message
    }

    // ===================================================
    // RETURN
    // ===================================================

    return {

      code:
        obj.type ===
        "validation"

          ? "validation"

          : "http_error",

      message,

      field_errors:
        Object.keys(
          fieldErrors
        ).length > 0

          ? fieldErrors

          : undefined,

      details: obj,
    }
  }

  // =====================================================
  // FALLBACK
  // =====================================================

  return {
    code: "network_error",
    message:
      "Произошла ошибка",
  }
}