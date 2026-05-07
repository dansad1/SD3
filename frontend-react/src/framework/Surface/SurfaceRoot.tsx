// src/framework/Surface/SurfaceRoot.tsx

import { useMemo } from "react"

import { SurfaceRenderer } from "./surfaceRenderer"
import { PageRoot } from "../layout/pageRoot"
import { appSurface } from "./appSurface"

import { FrameworkErrorBoundary } from "../trace/FrameworkErrorBoundary"
import { DevToolsRoot } from "../trace/DevtoolsRoot"
import { surfaceStore } from "./surfaceStore"

export function SurfaceRoot({
  children,
}: {
  children: React.ReactNode
}) {
  useMemo(() => {
    surfaceStore.ensure(appSurface)
  }, [])

  return (
    <>
      <DevToolsRoot />

      <PageRoot mode={appSurface.mode}>
        <FrameworkErrorBoundary>
          <SurfaceRenderer>
            {children}
          </SurfaceRenderer>
        </FrameworkErrorBoundary>
      </PageRoot>
    </>
  )
}