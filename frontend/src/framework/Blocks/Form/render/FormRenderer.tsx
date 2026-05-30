// src/framework/Blocks/Form/render/FormRenderer.tsx

import type {
  FormBlock,
  FormSchema,
} from "../types/types"

import { FieldRenderer }
  from "./FieldRenderer"

import { LayoutRenderer }
  from "./LayoutRenderer"

import type { Json }
  from "@/framework/types/json"

import type {
  ActionDescriptor,
} from "@/framework/Blocks/Action/types"

import {
  ActionBlock,
} from "@/framework/Blocks/Action/ActionBlock"

type Props = {

  schema: FormSchema

  values: Record<
    string,
    Json
  >

  fieldErrors?: Record<
    string,
    string[]
  >

  formError?: string | null

  onChange: (
    fieldId: string,
    value: Json
  ) => void

  actions?: ActionDescriptor[]
}

export function FormRenderer({
  schema,
  values,
  fieldErrors = {},
  formError,
  onChange,
  actions = [],

}: Props) {

  const density =
    schema.layout?.density ??
    "default"
console.log("FORM LAYOUT", schema.layout)
  console.log("FORM DENSITY", density)
  const preset =
    schema.layout?.preset ??
    "default"

  const render = (
    block: FormBlock
  ): React.ReactNode => {

    if (block.type === "field") {

      return (

        <div
          key={block.id}
          className="form-grid-item"
          style={{
            gridColumn:
              `span ${
                block.layout?.span ?? 12
              }`,
          }}
        >

          <FieldRenderer

            field={block.field}

            value={
              values[
                block.field.name
              ]
            }

            errors={
              fieldErrors[
                block.field.name
              ] ?? []
            }

            onChange={(v) =>
              onChange(
                block.field.name,
                v,
              )
            }
          />

        </div>
      )
    }

    return (

      <LayoutRenderer
        key={block.id}
        block={block}
        render={render}
      />
    )
  }

  const globalErrors =
    fieldErrors.__all__ ?? []

  const hasFieldErrors =
    Object.entries(fieldErrors)
      .some(([key, value]) => {

        return (
          key !== "__all__" &&
          value.length > 0
        )
      })

  const shouldShowFormError =
    !hasFieldErrors &&
    (
      Boolean(formError) ||
      globalErrors.length > 0
    )

  return (

    <form
      className={[
        "form",
        "form-grid",
        `form-layout-${preset}`,
        `form-density-${density}`,
      ].join(" ")}
    >

      {shouldShowFormError && (

        <div className="form-error">

          {formError && (
            <div>
              {formError}
            </div>
          )}

          {globalErrors.map(
            (
              error,
              index
            ) => (

              <div key={index}>
                {error}
              </div>
            )
          )}

        </div>

      )}

      {schema.blocks.map(render)}
      {actions.length > 0 && (
        <div className="form-actions">
          {actions.map(action => (
            <ActionBlock
              key={action.id}
              label={action.label}
              action={action.id}
              variant={
                action.variant ??
                "primary"
              }
            />

          ))}

        </div>

      )}

    </form>
  )
}