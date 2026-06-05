import type { Me } from "@/framework/auth/auth";
import type { PageRuntimeContext } from "@/framework/bind/types";
import type { ActionDescriptor } from "@/framework/Blocks/Action/types";

export function buildPageRuntimeContext(
  params: Record<string, string>,
  query: Record<string, string>,
  data: Record<string, unknown>,
  actions: ActionDescriptor[],
  user: Me | null,
): PageRuntimeContext {

  return {

    page: {
      params,
      query,
    },

    params,

    query,

    data,

    actions,

    user,

    me: user,

    can:
      user?.capabilities
      ?? {},
  }
}