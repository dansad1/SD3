import type { Me } from "@/framework/auth/auth"
import type { PageRuntimeContext } from "@/framework/bind/types"

export function buildPageRuntimeContext(
  params: Record<string, string>,
  query: Record<string, string>,
  data: Record<string, unknown>,
  user: Me | null
): PageRuntimeContext {
  return {
    page: {
      params,
      query,
    },

    params,
    query,
    data,

    user,
    me: user, // 👈 ВОТ ЭТО ДОБАВЬ
  }
}