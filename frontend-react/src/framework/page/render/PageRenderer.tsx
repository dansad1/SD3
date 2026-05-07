import { useUnsavedChangesGuard } from "@/framework/Blocks/hooks/useUnsavedChangesGuard"
import { TracePanel } from "@/framework/trace"
import { useState, useEffect } from "react"

import type { ApiPageSchema } from "../PageSchema"
import { usePageRuntime } from "../runtime/usePageRuntime"
import { PageView } from "./PageView"
import { usePageTrace } from "./usePageTrace"

import { PageContext } from "../context/context"
import { PageRuntimeContextProvider } from "../runtime/PageRuntimeContext"

export function PageRenderer({
  schema,
}: {
  schema: ApiPageSchema
}) {
  const pageKey = schema.id || schema.title || "page"

  usePageTrace(pageKey)

  const { ctrl, physicalTree } = usePageRuntime(schema)

  const [traceOpen, setTraceOpen] = useState(false)

  useUnsavedChangesGuard(ctrl.pageDirty)

  /* =========================
     HOTKEY
  ========================= */
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === "t") {
        setTraceOpen(v => !v)
      }
    }

    window.addEventListener("keydown", handler)
    return () => window.removeEventListener("keydown", handler)
  }, [])

  /* =========================
     RENDER
  ========================= */

  return (
    <PageRuntimeContextProvider value={ctrl.runtimeContext}>
      <PageContext.Provider value={ctrl.api}>

        <PageView
          schema={schema}
          physicalTree={physicalTree}
          actions={ctrl.actions}
          onToggleTrace={() => setTraceOpen(v => !v)}
        />

        <TracePanel
          open={traceOpen}
          onClose={() => setTraceOpen(false)}
        />

      </PageContext.Provider>
    </PageRuntimeContextProvider>
  )
}