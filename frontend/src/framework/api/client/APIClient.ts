// src/framework/api/client/APIClient.ts
import { FrameworkConfig } from "@/framework/config"
import { traceRuntime } from "@/framework/trace/runtime"
import { traceSessionStore } from "@/framework/trace/TraceSessionStore"
import { buildHeaders } from "./headers"
import {
  getErrorMessage,
  createApiError,
} from "./errorUtils"
import type { ApiError } from "@/framework/types/ApiError"

export class APIClient {
  private getBase(): string {
    return FrameworkConfig.apiBase.replace(/\/$/, "")
  }

  public buildUrl(path: string): string {
    const cleanPath = path.startsWith("/") ? path : `/${path}`
    return this.getBase() + cleanPath
  }

  private async request<T>(
    url: string,
    options: RequestInit = {}
  ): Promise<T> {
    const cleanPath = url.startsWith("/") ? url : `/${url}`
    const finalUrl = this.buildUrl(cleanPath)
    const method = (options.method || "GET").toUpperCase()

    const trace = traceRuntime.current()

    const doFetch = async (): Promise<T> => {
      const res = await fetch(finalUrl, {
        credentials: "include",
        cache: "no-store",
        ...options,
        headers: buildHeaders(options.headers),
      })

      const contentType =
        res.headers.get("content-type") || ""

      if (!res.ok) {
        const text = await res.text().catch(() => "")
        throw createApiError(res.status, contentType, text)
      }

      if (!contentType.includes("application/json")) {
        const error: ApiError = {
          code: "invalid_response",
          message: `Expected JSON, got "${contentType}"`,
          status: res.status,
        }
        throw error
      }

      return (await res.json()) as T
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
      } catch (e) {
        const message = getErrorMessage(e)

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

        throw e
      }
    }

    return trace.step(
      "api_request",
      doFetch,
      {
        api: cleanPath,
        method,
      }
    )
  }

  /* =========================
     HTTP METHODS
  ========================= */

  get<T>(url: string): Promise<T> {
    return this.request<T>(url)
  }

  post<T = void, B = unknown>(
    url: string,
    data?: B
  ): Promise<T> {
    let body: BodyInit | undefined
    let headers: HeadersInit | undefined

    if (data instanceof FormData) {
      body = data
    } else if (data !== undefined) {
      headers = { "Content-Type": "application/json" }
      body = JSON.stringify(data)
    }

    return this.request<T>(url, {
      method: "POST",
      body,
      headers,
    })
  }

  put<T = void, B = unknown>(
    url: string,
    data: B
  ): Promise<T> {
    let body: BodyInit
    let headers: HeadersInit | undefined

    if (data instanceof FormData) {
      body = data
    } else {
      headers = { "Content-Type": "application/json" }
      body = JSON.stringify(data)
    }

    return this.request<T>(url, {
      method: "PUT",
      body,
      headers,
    })
  }

  delete<T = void, B = unknown>(
    url: string,
    data?: B
  ): Promise<T> {
    let body: BodyInit | undefined
    let headers: HeadersInit | undefined

    if (data !== undefined) {
      headers = { "Content-Type": "application/json" }
      body = JSON.stringify(data)
    }

    return this.request<T>(url, {
      method: "DELETE",
      body,
      headers,
    })
  }
}