import type { BaseRow } from "../types/runtime"
import type {
  TableFeature,
  TableFeatureContext,
  FeaturePhase
} from "./types"

export function applyTableFeatures<T extends BaseRow>(
  ctx: TableFeatureContext<T>,
  features: TableFeature<T>[],
  phase: FeaturePhase
): TableFeatureContext<T> {

  let result = ctx

  for (const feature of features) {
    if (!feature) continue
    if (feature.phase !== phase) continue
    if (typeof feature.apply !== "function") continue

    try {
      const next = feature.apply(result)
      if (next) result = next
    } catch (e) {
      console.error("Table feature crash:", feature.name, e)
    }
  }

  return result
}