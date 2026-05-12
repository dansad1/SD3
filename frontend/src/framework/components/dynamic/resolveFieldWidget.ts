import type {
  FieldSchema,
  InteractionMode,
  Platform,
  RenderContext,
} from "@/framework/components/dynamic/types"

import type {
  WidgetKey,
} from "./resolvePrimitiveWidget"

import {
  resolvePrimitiveWidget,
} from "./resolvePrimitiveWidget"

import {
  resolveSemanticWidget,
} from "./semanticResolver"

export function resolveFieldWidget(
  field: FieldSchema,
  context: RenderContext,
  platform: Platform,
  interaction?: InteractionMode
): WidgetKey {
  const resolvedInteraction =
    interaction ??
    (field.readonly ? "readonly" : "editable")

  const semanticType =
    field.semantic?.type

  if (semanticType) {
    const semanticWidget =
      resolveSemanticWidget({
        field,
        semanticType,
        context,
        platform,
        interaction: resolvedInteraction,
        view: field.view,
        presentation: field.presentation,
      })

    if (semanticWidget) {
      return semanticWidget as WidgetKey
    }
  }

  return resolvePrimitiveWidget(field)
}