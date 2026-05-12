import type {
  ApiFormField,
} from "@/framework/api/form/types"

import type {
  FieldSchema,
} from "../types"
import { resolvePrimitiveWidget, type WidgetKey } from "../resolvePrimitiveWidget"
import { resolveSemanticWidget } from "../semanticResolver"



/* =========================================================
   NORMALIZE
========================================================= */

function normalizeField(
  field: ApiFormField
): FieldSchema {

  return {

    id:
      field.id ||
      field.name,

    name:
      field.name,

    label:
      field.label,

    help_text:
      field.help_text,

    widget:
      field.widget,

    semantic:
      field.semantic,

    view:
      field.view,

    presentation:
      field.presentation,

    html_type:
      field.html_type,

    choices:
      field.choices,

    entity:
      field.entity,

    multiple:
      field.multiple,

    columns:
      field.columns,

    required:
      field.required,

    readonly:
      field.readonly,
  }
}

/* =========================================================
   RESOLVE WIDGET
========================================================= */

export function resolveWidget(
  field: ApiFormField
): WidgetKey {

  const normalized =
    normalizeField(field)

  /* ========================================
     semantic resolution
  ======================================== */

  if (normalized.semantic?.type) {

    const semanticWidget =
      resolveSemanticWidget({

        field:
          normalized,

        semanticType:
          normalized.semantic.type,

        context:
          "form",

        platform:
          "desktop",

        interaction:
          normalized.readonly
            ? "readonly"
            : "editable",

        view:
          normalized.view,

        presentation:
          normalized.presentation,
      })

    if (semanticWidget) {
      return semanticWidget as WidgetKey
    }
  }

  /* ========================================
     primitive fallback
  ======================================== */

  return resolvePrimitiveWidget(
    normalized
  )
}