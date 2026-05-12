export * from "../DSL/blocks.generated"
export { page } from "../DSL/page"
// ==========================================================
// FRAMEWORK GLOBAL CONFIG
// ==========================================================

export const FrameworkConfig = {
  /**
   * Базовый URL API.
   *
   * Можно управлять через:
   * VITE_API_BASE=/api/entity
   *
   * По умолчанию — старый контракт (/api)
   */
  apiBase: import.meta.env.VITE_API_BASE || "/api",
}


// ==========================================================
// API URL BUILDER
// ==========================================================

export function buildApiUrl(path: string): string {
  const base = FrameworkConfig.apiBase.replace(/\/$/, "")
  const cleanPath = path.startsWith("/") ? path : `/${path}`
  return `${base}${cleanPath}`
}