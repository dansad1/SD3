import { useCallback } from "react"
import { useNavigate } from "react-router-dom"
import type { ActionContext } from "@/framework/Blocks/Action/types"
import { resolveWithContext } from "@/framework/bind/runtime/bindRuntime"
import { toPlainSnapshot } from "@/framework/bind/runtime/bindRuntime"
import type { PageRuntimeContext } from "@/framework/bind/types"

export function usePageNavigation(runtime: PageRuntimeContext) {
  const routerNavigate = useNavigate()

  const navigate = useCallback(
    (to: string, actionCtx: ActionContext = {}) => {
      if (!to) return

      const [rawPath, rawQuery = ""] = to.split("?")

      const redirectParams = new URLSearchParams(rawQuery)
      const finalParams = new URLSearchParams()

      // 🔥 resolve через переданный runtime
      const snapshot = toPlainSnapshot(actionCtx)
      const resolved = resolveWithContext(snapshot, runtime)

      for (const [k, v] of Object.entries(resolved)) {
        if (
          v !== null &&
          v !== undefined &&
          (typeof v === "string" ||
            typeof v === "number" ||
            typeof v === "boolean")
        ) {
          finalParams.set(k, String(v))
        }
      }

      for (const [k, v] of redirectParams.entries()) {
        finalParams.set(k, v)
      }

      const query = finalParams.toString()
      const encodedPath = encodeURIComponent(rawPath)

      const url = rawPath.startsWith("/")
        ? (query ? `${rawPath}?${query}` : rawPath)
        : (query
            ? `/page/${encodedPath}?${query}`
            : `/page/${encodedPath}`)

      routerNavigate(url)
    },
    [routerNavigate, runtime]
  )

  return { navigate }
}