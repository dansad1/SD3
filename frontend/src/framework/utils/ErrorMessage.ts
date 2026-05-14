// framework/utils/ErrorMessage.ts

import type { ApiError }
  from "../types/ApiError"

export function getApiErrorMessage(
  error: ApiError
) {

  // =====================
  // FIELD ERRORS
  // =====================

  if (error.field_errors) {

    const firstFieldErrors =
      Object.values(
        error.field_errors
      )[0]

    const firstError =
      firstFieldErrors?.[0]

    if (firstError) {
      return firstError
    }
  }

  // =====================
  // CODE ERRORS
  // =====================

  switch (error.code) {

    case "validation":
      return (
        error.message ||
        "Ошибка валидации"
      )

    case "http_error":
      return (
        error.message ||
        "Ошибка запроса"
      )

    case "network_error":
      return (
        "Нет соединения с сервером"
      )

    case "invalid_response":
      return (
        "Некорректный ответ сервера"
      )

    case "not_modified":
      return (
        "Изменений нет"
      )

    default:
      return (
        error.message ||
        "Произошла ошибка"
      )
  }
}