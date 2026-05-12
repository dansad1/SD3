import type {
  FieldSchema,
  InteractionMode,
  Platform,
  PresentationNode,
  RenderContext,
  RenderView,
} from "@/framework/components/dynamic/types"

export type SemanticResolveInput = {
  field: FieldSchema

  semanticType: string

  context: RenderContext
  platform: Platform
  interaction: InteractionMode

  view?: RenderView
  presentation?: PresentationNode
}

export type SemanticResolverFn = (
  input: SemanticResolveInput
) => string | null

let resolver: SemanticResolverFn | null = null

export function registerSemanticResolver(
  fn: SemanticResolverFn
) {
  resolver = fn
}

export function resolveSemanticWidget(
  input: SemanticResolveInput
): string | null {
  if (!resolver) return null

  return resolver(input)
}