// src/framework/Surface/surface.ts

export type SurfaceMode = "auth" | "app"

export type SurfaceArea =
  | "topbar"
  | "main"
  | "overlay"
  | "drawer"
  | "toast"
  | "bottomNav"

export type SurfaceContent =
  | { type: "empty" }
  | { type: "page" }
  | { type: "overlay" }
  | { type: "drawer" }
  | { type: "toast" }

export type SurfaceTopbarState = {
  visible?: boolean
  title?: string
  subtitle?: string
  back?: boolean
  actions?: Array<{
    id: string
    icon?: string
    label?: string
    action: string
  }>
}

export type SurfaceOverlayState = {
  open: boolean
  component?: string
  payload?: Record<string, unknown>
}

export type SurfaceDrawerState = {
  open: boolean
  component?: string
  side?: "left" | "right" | "bottom"
  payload?: Record<string, unknown>
}

export type SurfaceSchema = {
  mode: SurfaceMode

  areas: Partial<
    Record<SurfaceArea, SurfaceContent>
  >

  topbar?: SurfaceTopbarState
  overlay?: SurfaceOverlayState
  drawer?: SurfaceDrawerState

  options?: {
    hideSidebarOnMobile?: boolean
    lockScrollOnOverlay?: boolean
  }
}