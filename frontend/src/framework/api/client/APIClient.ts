// src/framework/api/client/APIClient.ts

import { FrameworkConfig } from "@/framework/config"
import { traceRuntime } from "@/framework/trace/runtime"
import { traceSessionStore } from "@/framework/trace/TraceSessionStore"
import type { ApiError } from "@/framework/types/ApiError"

import {
  createApiError,
  getErrorMessage,
} from "./errorUtils"
import { buildHeaders } from "./headers"
import { ensureCSRFCookie } from "@/framework/utils/ensureCSRFCookie"


const UNSAFE_METHODS = new Set([
  "POST",
  "PUT",
  "PATCH",
  "DELETE",
])


export class APIClient {
  private getBase(): string {
    return FrameworkConfig.apiBase.replace(
      /\/$/,
      "",
    )
  }

  public buildUrl(
    path: string,
  ): string {
    const cleanPath = path.startsWith("/")
      ? path
      : `/${path}`

    return this.getBase() + cleanPath
  }

  private async request<T>(
    url: string,
    options: RequestInit = {},
  ): Promise<T> {
    const cleanPath = url.startsWith("/")
      ? url
      : `/${url}`

    const finalUrl = this.buildUrl(
      cleanPath,
    )

    const method = (
      options.method
      || "GET"
    ).toUpperCase()

    const trace = traceRuntime.current()

    const doFetch = async (): Promise<T> => {
      /*
       * Django требует CSRF-cookie и заголовок
       * X-CSRFToken для изменяющих запросов.
       *
       * Сначала получаем cookie, затем buildHeaders()
       * читает её и добавляет заголовок.
       */
      if (UNSAFE_METHODS.has(method)) {
        await ensureCSRFCookie()
      }

      const response = await fetch(
        finalUrl,
        {
          credentials: "include",
          cache: "no-store",
          ...options,
          headers: buildHeaders(
            options.headers,
          ),
        },
      )

      const contentType = (
        response.headers.get(
          "content-type",
        )
        || ""
      )

      if (!response.ok) {
        const text = await response
          .text()
          .catch(() => "")

        throw createApiError(
          response.status,
          contentType,
          text,
        )
      }

      if (
        !contentType.includes(
          "application/json",
        )
      ) {
        const error: ApiError = {
          code: "invalid_response",
          message: (
            `Expected JSON, got "${contentType}"`
          ),
          status: response.status,
        }

        throw error
      }

      return await response.json() as T
    }

    if (!trace) {
      const started = Date.now()

      try {
        const result = await doFetch()

        traceSessionStore.push({
          id: crypto.randomUUID(),
          page: window.location.pathname,
          trigger: "request",
          status: "ok",
          startedAt: started,
          finishedAt: Date.now(),
          summary: `${method} ${cleanPath}`,
          root: {
            id: crypto.randomUUID(),
            name: "api_request",
            status: "ok",
            startedAt: started,
            finishedAt: Date.now(),
            meta: {
              api: cleanPath,
              method,
            },
            children: [],
          },
        })

        return result
      } catch (error) {
        const message = getErrorMessage(
          error,
        )

        traceSessionStore.push({
          id: crypto.randomUUID(),
          page: window.location.pathname,
          trigger: "request",
          status: "error",
          startedAt: started,
          finishedAt: Date.now(),
          summary: `${method} ${cleanPath}`,
          root: {
            id: crypto.randomUUID(),
            name: "api_request",
            status: "error",
            startedAt: started,
            finishedAt: Date.now(),
            meta: {
              api: cleanPath,
              method,
              error: message,
            },
            children: [],
          },
        })

        throw error
      }
    }

    return trace.step(
      "api_request",
      doFetch,
      {
        api: cleanPath,
        method,
      },
    )
  }

  // =====================================================
  // HTTP METHODS
  // =====================================================

  get<T>(
    url: string,
  ): Promise<T> {
    return this.request<T>(
      url,
    )
  }

  post<
    T = void,
    B = unknown,
  >(
    url: string,
    data?: B,
  ): Promise<T> {
    const request = this.buildBody(
      data,
    )

    return this.request<T>(
      url,
      {
        method: "POST",
        body: request.body,
        headers: request.headers,
      },
    )
  }

  put<
    T = void,
    B = unknown,
  >(
    url: string,
    data: B,
  ): Promise<T> {
    const request = this.buildBody(
      data,
    )

    return this.request<T>(
      url,
      {
        method: "PUT",
        body: request.body,
        headers: request.headers,
      },
    )
  }

  patch<
    T = void,
    B = unknown,
  >(
    url: string,
    data: B,
  ): Promise<T> {
    const request = this.buildBody(
      data,
    )

    return this.request<T>(
      url,
      {
        method: "PATCH",
        body: request.body,
        headers: request.headers,
      },
    )
  }

  delete<
    T = void,
    B = unknown,
  >(
    url: string,
    data?: B,
  ): Promise<T> {
    const request = this.buildBody(
      data,
    )

    return this.request<T>(
      url,
      {
        method: "DELETE",
        body: request.body,
        headers: request.headers,
      },
    )
  }

  // =====================================================
  // BODY
  // =====================================================

  private buildBody<B>(
    data?: B,
  ): {
    body: BodyInit | undefined
    headers: HeadersInit | undefined
  } {
    if (data === undefined) {
      return {
        body: undefined,
        headers: undefined,
      }
    }

    if (data instanceof FormData) {
      return {
        body: data,
        headers: undefined,
      }
    }

    return {
      body: JSON.stringify(
        data,
      ),
      headers: {
        "Content-Type": "application/json",
      },
    }
  }
}