import type {
  FieldSchema,
} from "./types"
import { resolveWidget } from "./widgets/resolveWidget"




export function validateFieldSchema(
  field: FieldSchema
) {

  /* ===============================
     object
  =============================== */

  if (

    !field ||

    typeof field !== "object"

  ) {

    throw new Error(

      "Invalid field schema"

    )

  }


  /* ===============================
     name
  =============================== */

  if (

    !field.name ||

    typeof field.name !== "string"

  ) {

    throw new Error(

      'Field must have a valid "name"'

    )

  }


  /* ===============================
     widget
  =============================== */

  if (

    !field.widget ||

    typeof field.widget !== "string"

  ) {

    throw new Error(

      `Field "${

        field.name

      }" has no valid widget`

    )

  }


  /* ===============================
     resolvable widget
  =============================== */

  try {

    resolveWidget(

      field,

    )

  }

  catch {

    throw new Error(

      `Unknown widget "${

        field.widget

      }" in field "${

        field.name

      }"`

    )

  }


  /* ===============================
     options
  =============================== */

  if (

    field.options &&

    !Array.isArray(

      field.options

    )

  ) {

    throw new Error(

      `Invalid options for field "${

        field.name

      }"`

    )

  }


  /* ===============================
     label
  =============================== */

  if (

    field.label &&

    typeof field.label !== "string"

  ) {

    throw new Error(

      `Invalid label for field "${

        field.name

      }"`

    )

  }


  /* ===============================
     required
  =============================== */

  if (

    field.required !== undefined &&

    typeof field.required !== "boolean"

  ) {

    throw new Error(

      `Invalid required flag in field "${

        field.name

      }"`

    )

  }


  /* ===============================
     readonly
  =============================== */

  if (

    field.readonly !== undefined &&

    typeof field.readonly !== "boolean"

  ) {

    throw new Error(

      `Invalid readonly flag in field "${

        field.name

      }"`

    )

  }


  /* ===============================
     multiple consistency
  =============================== */

  if (

    field.multiple

  ) {

    if (

      !field.options &&

      !field.entity

    ) {

      console.warn(

        `Field "${

          field.name

        }" is multiple but has no options or entity`

      )

    }

  }


  /* ===============================
     relation consistency
  =============================== */

  if (

    field.entity &&

    field.options

  ) {

    console.warn(

      `Field "${

        field.name

      }" has both entity and options (entity will be ignored)`

    )

  }


  /* ===============================
     html_type
  =============================== */

  if (

    field.html_type &&

    typeof field.html_type !== "string"

  ) {

    throw new Error(

      `Invalid html_type in field "${

        field.name

      }"`

    )

  }

}