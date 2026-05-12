export type ApiError = {
  code:
    | "http_error"
    | "invalid_response"
    | "network_error"
    | "not_modified"

  message: string
  status?: number
  field_errors?: Record<string, string>
  details?: unknown
}