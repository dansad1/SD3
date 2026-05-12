// framework/utils/ErrorMessage.ts

import type { ApiError } from "../types/ApiError"

export function getApiErrorMessage(
  error: ApiError
) {
  switch (error.code) {
    case "http_error":
      return error.message || "Ошибка запроса"

    case "network_error":
      return "Нет соединения с сервером"

    case "invalid_response":
      return "Некорректный ответ сервера"

    case "not_modified":
      return "Изменений нет"

    default:
      return error.message || "Произошла ошибка"
  }
}