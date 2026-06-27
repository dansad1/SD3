// resolveWidget.ts

import type {
  FieldSchema,
} from "../types"

import {
  resolvePrimitiveWidget,
  type WidgetKey,
} from "../resolvePrimitiveWidget"

import {
  resolveSemanticWidget,
} from "../semanticResolver"


/* =========================================================
   RESOLVE WIDGET
========================================================= */

export function resolveWidget(
  field: FieldSchema
): WidgetKey {

 

  /* ========================================
     semantic resolution
  ======================================== */

  if (field.semantic?.type) {

    const semanticWidget =
      resolveSemanticWidget({

        field,

        semanticType:
          field.semantic.type,

        context:
          "form",

        platform:
          "desktop",

        interaction:
          field.readonly
            ? "readonly"
            : "editable",

        view:
          field.view,

        presentation:
          field.presentation,
      })

    console.log(
      "🧠 semanticWidget",
      semanticWidget
    )

    if (semanticWidget) {
      return semanticWidget as WidgetKey
    }
  }

  /* ========================================
     primitive fallback
  ======================================== */

  const primitive =
    resolvePrimitiveWidget(field)

  

  return primitive
}