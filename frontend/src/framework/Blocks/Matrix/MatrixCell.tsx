import React from "react"

import { getSemanticRenderer }
  from "@/framework/renderers/getRenderer"

import { NumberCell }
  from "./Cells/NumberCell"

import { SelectCell }
  from "./Cells/SelectCell"

import { TextCell }
  from "./Cells/TextCell"

import type {
  MatrixCellSchema,
  MatrixCellValue,
} from "./types"

type Props = {
  schema?: MatrixCellSchema

  value: MatrixCellValue

  onChange: (
    patch: Partial<MatrixCellValue>
  ) => void
}

/* =========================================================
   BUILTIN WIDGET RESOLUTION
========================================================= */

function resolveBuiltinWidget(
  schema: MatrixCellSchema | undefined,
  value: MatrixCellValue,
): MatrixCellSchema["widget"] {

  if (schema?.widget) {
    return schema.widget
  }

  if (typeof value?.value === "number") {
    return "number"
  }

  if (typeof value?.value === "string") {
    return "text"
  }

  return "text"
}

/* =========================================================
   MATRIX CELL
========================================================= */

export const MatrixCell = ({
  schema,
  value,
  onChange,
}: Props) => {

  /* ========================================
     semantic renderer
  ======================================== */

  const semanticType =
    schema?.semantic?.type

  if (semanticType) {

    const renderer =
      getSemanticRenderer(
        semanticType,
        "matrix",
        "desktop",
      )

    if (renderer) {

      return React.createElement(
        renderer,
        {
          value,

          onChange: (
            next: unknown
          ) => {

            onChange(
              next as Partial<MatrixCellValue>
            )
          },

          context: "matrix",

          platform: "desktop",

          presentation:
            schema?.presentation,
        }
      )
    }
  }

  /* ========================================
     builtin primitive widgets
  ======================================== */

  const widget =
    resolveBuiltinWidget(
      schema,
      value,
    )

  switch (widget) {

    case "select":
      return (
        <SelectCell
          schema={schema}
          value={value}
          onChange={onChange}
        />
      )

    case "number":
      return (
        <NumberCell
          value={value}
          onChange={onChange}
        />
      )

    case "text":
    default:
      return (
        <TextCell
          value={value}
          onChange={onChange}
        />
      )
  }
}