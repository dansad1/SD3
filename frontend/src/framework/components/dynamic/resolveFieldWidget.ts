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

  console.log(
    "🔵 resolveFieldWidget INPUT",
    {
      name: field.name,
      type: field.type,
      widget: field.widget,
      presentation: field.presentation,
      options: field.options,
      entity: field.entity,
      multiple: field.multiple,
      readonly: field.readonly,
      semantic: field.semantic,
    }
  )

  /* ========================================
     presentation layer
  ======================================== */

  if (field.presentation === "meta") {

    console.log(
      "🟡 resolveFieldWidget META",
      {
        name: field.name,
      }
    )

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

      console.log(
        "🟢 resolveFieldWidget SEMANTIC",
        {
          name: field.name,
          semanticType,
          widget: semanticWidget,
        }
      )

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

  console.log(
    "🟣 resolveFieldWidget RESULT",
    {
      name: field.name,
      type: field.type,
      widgetFromSchema:
        field.widget,
      resolvedWidget:
        widget,
      options:
        field.options,
    }
  )

  return widget
}