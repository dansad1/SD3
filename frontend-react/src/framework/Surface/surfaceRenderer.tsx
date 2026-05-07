// src/framework/Surface/surfaceRenderer.tsx

import {
  type ReactNode,
  useSyncExternalStore,
} from "react"

import { NavPanel } from "../components/ui/NavPanel"
import { surfaceStore } from "./surfaceStore"
import type { SurfaceArea } from "./surface"

const AREAS: SurfaceArea[] = [
  "topbar",
  "main",
  "overlay",
  "drawer",
]

export function SurfaceRenderer({
  children,
}: {
  children?: ReactNode
}) {
  useSyncExternalStore(
    surfaceStore.subscribe.bind(surfaceStore),
    () => surfaceStore.get(),
    () => surfaceStore.get()
  )

  if (!surfaceStore.has()) {
    return null
  }

  return (
    <div className="surface surface-app">
      {AREAS.map(area => {
        const node = renderArea(area, children)

        if (!node) {
          return null
        }

        return (
          <div key={area}>
            {node}
          </div>
        )
      })}
    </div>
  )
}

function renderArea(
  area: SurfaceArea,
  children?: ReactNode
) {
  const surface = surfaceStore.get()

  if (area === "topbar") {
    return (
      <div className="surface-area topbar">
        <NavPanel />
      </div>
    )
  }

  if (area === "main") {
    return (
      <div className="surface-area main">
        {children}
      </div>
    )
  }

  if (area === "overlay") {
    if (!surface.overlay?.open) {
      return null
    }

    return (
      <div className="surface-area overlay is-open">
        <div className="surface-overlay-backdrop" />

        <div className="surface-overlay-panel">
          <div className="surface-overlay-placeholder">
            Overlay:{" "}
            {surface.overlay.component}
          </div>
        </div>
      </div>
    )
  }

  if (area === "drawer") {
    if (!surface.drawer?.open) {
      return null
    }

    return (
      <div
        className={[
          "surface-drawer",
          `surface-drawer-${surface.drawer.side ?? "right"}`,
        ].join(" ")}
      >
        <div className="surface-drawer-placeholder">
          Drawer:{" "}
          {surface.drawer.component}
        </div>
      </div>
    )
  }

  return null
}