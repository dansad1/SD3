import type { FormBlock, FormSchema } from "../types/types"
import { FieldRenderer } from "./FieldRenderer"
import { LayoutRenderer } from "./LayoutRenderer"
import type { Json } from "@/framework/types/json"

type Props = {
  schema: FormSchema
  values: Record<string, Json>
  onChange: (fieldId: string, value: Json) => void
}

export function FormRenderer({
  schema,
  values,
  onChange,
}: Props) {

  const render = (block: FormBlock): React.ReactNode => {

    if (block.type === "field") {
      return (
        <div
          key={block.id}
          className="form-grid-item"
          style={{
            gridColumn: `span ${block.layout?.span ?? 12}`,
          }}
        >
          <FieldRenderer
            field={block.field}
            value={values[block.field.name]}
            onChange={(v) => onChange(block.field.name, v)}
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

  return (
    <form className="form-grid">
      {schema.blocks.map(render)} {/* 👈 без processors */}
    </form>
  )
}