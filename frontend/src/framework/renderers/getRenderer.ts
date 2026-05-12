
import type {
  SemanticRenderer,
} from "./types"

import {
  semanticRendererRegistry,
} from "./registry"

import {
  resolveSemanticRenderer,
} from "./semanticResolver"
import type { Platform, RenderContext } from "../components/dynamic/types"

export function getSemanticRenderer(
  semanticType: string,
  context: RenderContext,
  platform: Platform,
): SemanticRenderer | null {

  const key =
    resolveSemanticRenderer(
      semanticType,
      context,
      platform,
    )

  if (!key) {
    return null
  }

  return (
    semanticRendererRegistry[key] ||
    null
  )
}