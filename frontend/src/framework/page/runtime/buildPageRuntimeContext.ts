// src/framework/page/runtime/buildPageRuntimeContext.ts

import type { Me }
  from "@/framework/auth/auth"

import type { ActionDescriptor }
  from "@/framework/Blocks/Action/types"

import type { PageRuntimeContext }
  from "@/framework/bind/types"


export function buildPageRuntimeContext(

  params: Record<string, string>,

  query: Record<string, string>,

  data: Record<string, unknown>,

  actions: ActionDescriptor[],

  user: Me | null,

): PageRuntimeContext {

  return {

    // =====================================================
    // PAGE
    // =====================================================

    page: {
      params,
      query,
    },

    // =====================================================
    // ROUTE
    // =====================================================

    params,

    query,

    // =====================================================
    // DATA
    // =====================================================

    data,

    // =====================================================
    // ACTIONS
    // =====================================================

    actions,

    // =====================================================
    // USER
    // =====================================================

    user,

    me: user,
  }
}