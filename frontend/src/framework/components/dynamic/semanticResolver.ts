import type {
  FieldSchema,
  InteractionMode,
  Platform,
  PresentationNode,
  RenderContext,
  RenderView,
} from "@/framework/components/dynamic/types"

import type {
  WidgetKey,
} from "./registry"

/* =========================================================
   INPUT
========================================================= */

export type SemanticResolveInput = {

  field: FieldSchema

  semanticType: string

  context: RenderContext

  platform: Platform

  interaction: InteractionMode

  view?: RenderView

  presentation?: PresentationNode
}

/* =========================================================
   RESOLVER
========================================================= */

export type SemanticResolverFn = (
  input: SemanticResolveInput
) => WidgetKey | null

/* =========================================================
   RUNTIME
========================================================= */

let resolver:
  SemanticResolverFn
  | null = null

/* =========================================================
   REGISTER
========================================================= */

export function registerSemanticResolver(
  fn: SemanticResolverFn
) {

  resolver = fn
}

/* =========================================================
   RESOLVE
========================================================= */

export function resolveSemanticWidget(
  input: SemanticResolveInput
): WidgetKey | null {

  if (!resolver) {
    return null
  }

  return resolver(input)
}