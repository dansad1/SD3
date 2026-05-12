import type {
  SemanticRenderer
} from "./types"

export const semanticRendererRegistry:
  Record<string, SemanticRenderer> = {}