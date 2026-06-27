import type {
  FieldSchema,
  InteractionMode,
  Platform,
  RenderContext,
} from "@/framework/components/dynamic/types"

import type {
  WidgetKey,
} from "./registry"

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

 

  /* ========================================
     presentation layer
  ======================================== */

  if (field.presentation === "meta") {

   

    return "Meta"
  }

  /* ========================================
     interaction
  ======================================== */

  const resolvedInteraction =
    interaction ??
    (
      field.readonly
        ? "readonly"
        : "editable"
    )

  /* ========================================
     semantic layer
  ======================================== */

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


      return semanticWidget
    }
  }

  /* ========================================
     primitive layer
  ======================================== */

  const widget =
    resolvePrimitiveWidget(
      field
    )

 

  return widget
}