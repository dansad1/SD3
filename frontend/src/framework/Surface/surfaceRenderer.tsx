// src/framework/Surface/surfaceRenderer.tsx

import {
  type ReactNode,
  useSyncExternalStore,
} from "react"



import { surfaceStore }
  from "./surfaceStore"

import type {
  SurfaceArea,
} from "./surface"
import { NavPanel } from "../components/ui/Navpanel"


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

  const surface =
    surfaceStore.get()

  if (!surface) {
    return null
  }

  const className = [

    "surface",

    `surface-${surface.mode}`,

  ]
    .filter(Boolean)
    .join(" ")

  return (

    <div className={className}>

      {AREAS.map(area => {

        const node = renderArea(
          surface,
          area,
          children
        )

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

  surface: ReturnType<typeof surfaceStore.get>,

  area: SurfaceArea,

  children?: ReactNode
) {

  if (!surface) {
    return null
  }

  const areaConfig =
    surface.areas?.[area]

  // =====================================================
  // EMPTY AREA
  // =====================================================

  if (

    !areaConfig ||

    areaConfig.type === "empty"

  ) {
    return null
  }

  // =====================================================
  // TOPBAR
  // =====================================================

  if (area === "topbar") {

    return (

      <div className="surface-area topbar">

        <NavPanel />

      </div>
    )
  }

  // =====================================================
  // MAIN
  // =====================================================

  if (area === "main") {

    return (

      <div className="surface-area main">

        {children}

      </div>
    )
  }

  // =====================================================
  // OVERLAY
  // =====================================================

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

  // =====================================================
  // DRAWER
  // =====================================================

  if (area === "drawer") {

    if (!surface.drawer?.open) {
      return null
    }

    return (

      <div
        className={[

          "surface-drawer",

          `surface-drawer-${
            surface.drawer.side ?? "right"
          }`,

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