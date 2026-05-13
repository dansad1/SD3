import { useUnsavedChangesGuard }
  from "@/framework/Blocks/hooks/useUnsavedChangesGuard"

import { TracePanel }
  from "@/framework/trace"

import {
  useState,
  useEffect,
} from "react"

import type { ApiPageSchema }
  from "../PageSchema"

import { usePageRuntime }
  from "../runtime/usePageRuntime"

import { PageView }
  from "./PageView"

import { usePageTrace }
  from "./usePageTrace"

import { PageContext }
  from "../context/context"

import { PageRuntimeContextProvider }
  from "../runtime/PageRuntimeContext"

import { usePageSurface }
  from "@/framework/Surface/usePageSurface"


export function PageRenderer({
  schema,
}: {
  schema: ApiPageSchema
}) {

  // =====================================================
  // PAGE KEY
  // =====================================================

  const pageKey =
    schema.id ||
    schema.title ||
    "page"

  // =====================================================
  // TRACE
  // =====================================================

  usePageTrace(pageKey)

  // =====================================================
  // SURFACE
  // =====================================================

  usePageSurface(
    schema.chrome
  )

  // =====================================================
  // RUNTIME
  // =====================================================

  const {
    ctrl,
    physicalTree,
  } = usePageRuntime(schema)

  // =====================================================
  // TRACE PANEL
  // =====================================================

  const [
    traceOpen,
    setTraceOpen,
  ] = useState(false)

  // =====================================================
  // UNSAVED CHANGES
  // =====================================================

  useUnsavedChangesGuard(
    ctrl.pageDirty
  )

  // =====================================================
  // HOTKEYS
  // =====================================================

  useEffect(() => {

    const handler = (
      e: KeyboardEvent
    ) => {

      if (

        e.ctrlKey &&

        e.shiftKey &&

        e.key.toLowerCase() === "t"

      ) {

        setTraceOpen(
          v => !v
        )
      }
    }

    window.addEventListener(
      "keydown",
      handler
    )

    return () => {

      window.removeEventListener(
        "keydown",
        handler
      )
    }

  }, [])

  // =====================================================
  // RENDER
  // =====================================================

  return (

    <PageRuntimeContextProvider
      value={ctrl.runtimeContext}
    >

      <PageContext.Provider
        value={ctrl.api}
      >

        <PageView

          schema={schema}

          physicalTree={physicalTree}

          actions={ctrl.actions}

          onToggleTrace={() =>
            setTraceOpen(v => !v)
          }
        />

        <TracePanel

          open={traceOpen}

          onClose={() =>
            setTraceOpen(false)
          }
        />

      </PageContext.Provider>

    </PageRuntimeContextProvider>
  )
}