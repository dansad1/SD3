// src/framework/Blocks/Table/features/registry.ts

import type { TableFeature } from "./types"
import type { BaseRow } from "../types/runtime"
import { initTableFeatures } from "./init"

const registry: TableFeature<BaseRow>[] = []

let initialized = false

export function registerTableFeature<T extends BaseRow>(
  feature: TableFeature<T>
) {
  registry.push(feature as TableFeature<BaseRow>)
}

export function getTableFeatures<T extends BaseRow>() {
  // 🔥 ГАРАНТИЯ что фичи есть
  if (!initialized) {
    initialized = true
    initTableFeatures()
  }

  return registry as TableFeature<T>[]
}