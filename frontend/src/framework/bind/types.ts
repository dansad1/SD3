// src/framework/bind/types.ts

import type { Me } from "../auth/auth"

export type BindValue = {
  bind: string
}

export type PageRuntimeContext = {
  page: {
    params: Record<string, string>
    query: Record<string, string>
  }

  params: Record<string, string>
  query: Record<string, string>
  data: Record<string, unknown>

  user?: Me | null
  me?: Me | null // 👈 ВОТ ЭТО ДОБАВЬ
}

export type BindScope = {
  query?: Record<string, unknown>
  params?: Record<string, unknown>

  user?: Record<string, unknown>
  me?: Record<string, unknown> // 👈 ВОТ ЭТО КРИТИЧНО

  page?: Record<string, unknown>
  data?: Record<string, unknown>

  form?: {
    entity?: string
    values: Record<string, unknown>
  }

  list?: {
    rows?: unknown[]
    selected?: unknown[]
  }

  row?: Record<string, unknown>

  [key: string]: unknown
}

export type AnyBlock = Record<string, unknown>
export type BindResult = AnyBlock | AnyBlock[] | null