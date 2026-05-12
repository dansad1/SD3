import { createEmitter } from "./core/emitter"
import { createSurfaceState } from "./core/state"

import { createAreaModule } from "./modules/area"
import { createOverlayModule } from "./modules/overlay"
import { createDrawerModule } from "./modules/drawer"
import { createTopbarModule } from "./modules/topbar"
import { createOptionsModule } from "./modules/options"

import type {
  SurfaceSchema,
  SurfaceArea,
} from "./surface"

class SurfaceStore {
  private emitter = createEmitter()
  private state = createSurfaceState(null)

  /* INIT */

  init(surface: SurfaceSchema) {
    this.state.set(structuredClone(surface))
    this.emitter.emit()
  }
  ensure(surface: SurfaceSchema) {
  if (!this.state.get()) {
    this.state.set(structuredClone(surface))
    this.emitter.emit()
  }
}

  reset(surface?: SurfaceSchema) {
    this.state.set(
      surface ? structuredClone(surface) : null
    )
    this.emitter.emit()
  }

  /* GET */

  get() {
    return this.state.get()
  }

  has() {
    return !!this.state.get()
  }

  getArea(area: SurfaceArea) {
    return this.state.get()?.areas?.[area]
  }

  /* MODULES */

  private area = createAreaModule(
    this.state.update,
    this.emitter.emit
  )

  private overlay = createOverlayModule(
    this.state.update,
    this.emitter.emit
  )

  private drawer = createDrawerModule(
    this.state.update,
    this.emitter.emit
  )

  private topbar = createTopbarModule(
    this.state.update,
    this.emitter.emit
  )

  private options = createOptionsModule(
    this.state.update,
    this.emitter.emit
  )

  /* PUBLIC API */

  setArea = this.area.setArea
  clearArea = this.area.clearArea
  clearAreas = this.area.clearAreas

  setOverlay = this.overlay.setOverlay
  openOverlay = this.overlay.openOverlay
  closeOverlay = this.overlay.closeOverlay
  clearOverlay = this.overlay.clearOverlay

  setDrawer = this.drawer.setDrawer
  openDrawer = this.drawer.openDrawer
  closeDrawer = this.drawer.closeDrawer
  clearDrawer = this.drawer.clearDrawer

  setTopbar = this.topbar.setTopbar
  clearTopbar = this.topbar.clearTopbar

  setOptions = this.options.setOptions

  subscribe = this.emitter.subscribe
}

export const surfaceStore = new SurfaceStore()