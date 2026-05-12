import type { TableApiBlock } from "../types/api"
import type { BaseRow } from "../types/runtime"
import { getTableFeatures } from "./registry"
import type { TableFeature } from "./types"

export function collectTableFeatures<T extends BaseRow>(
  block: TableApiBlock
): TableFeature<T>[] {
  const all = getTableFeatures() as TableFeature<T>[]

  return all.filter(f => {
    // 🔥 core features всегда включены
    if (f.name === "toolbar") return true

    // 🔥 optional
    return !!block.features?.[f.name as keyof typeof block.features]
  })
}