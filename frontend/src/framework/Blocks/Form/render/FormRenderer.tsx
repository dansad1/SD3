// src/framework/Blocks/Form/render/FormRenderer.tsx

import type { FormBlock, FormSchema } from "../types/types"

import { FieldRenderer } from "./FieldRenderer"
import { LayoutRenderer } from "./LayoutRenderer"

import type { Json } from "@/framework/types/json"

import type { ActionDescriptor } from "@/framework/Blocks/Action/types"

import { ActionBlock } from "@/framework/Blocks/Action/ActionBlock"


type Props = {

  schema: FormSchema

  values: Record<string, Json>

  onChange: (
    fieldId: string,
    value: Json
  ) => void

  actions?: ActionDescriptor[]
}


export function FormRenderer({
  schema,
  values,
  onChange,

  actions = [],

}: Props) {

  // =====================================================
  // BLOCK RENDER
  // =====================================================

  const render = (
    block: FormBlock
  ): React.ReactNode => {

    // ===================================================
    // FIELD
    // ===================================================

    if (block.type === "field") {

      return (
        <div
          key={block.id}
          className="form-grid-item"
          style={{
            gridColumn:
              `span ${block.layout?.span ?? 12}`,
          }}
        >

          <FieldRenderer
            field={block.field}
            value={values[block.field.name]}
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

    // ===================================================
    // LAYOUT
    // ===================================================

    return (
      <LayoutRenderer
        key={block.id}
        block={block}
        render={render}
      />
    )
  }

  // =====================================================
  // RENDER
  // =====================================================

  return (

    <form className="form-grid">

      {schema.blocks.map(render)}

      {/* ============================================= */}
      {/* FORM ACTIONS */}
      {/* ============================================= */}

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