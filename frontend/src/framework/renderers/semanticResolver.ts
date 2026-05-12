import type { Platform, RenderContext } from "../components/dynamic/types"


export type SemanticRendererResolverFn = (
  semanticType: string,
  context: RenderContext,
  platform: Platform,
) => string | null

let resolver:
  SemanticRendererResolverFn | null = null

export function registerSemanticRendererResolver(
  fn: SemanticRendererResolverFn
) {
  resolver = fn
}

export function resolveSemanticRenderer(
  semanticType: string,
  context: RenderContext,
  platform: Platform,
): string | null {

  if (!resolver) {
    return null
  }

  return resolver(
    semanticType,
    context,
    platform,
  )
}