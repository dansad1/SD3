import type {
  FormSectionBlock,
  FormBlock,
} from "../types/types"

type Props = {
  block: FormSectionBlock

  render: (
    block: FormBlock
  ) => React.ReactNode
}

export function FormSectionRenderer({
  block,
  render,
}: Props) {

  return (
    <section
      className="form-section form-grid"
      style={{
        gridColumn: `span ${block.layout?.span ?? 12}`,
        order: block.layout?.order,
      }}
    >

      {(block.title ||
        block.description) && (
        <div className="form-section-header">

          {block.title && (
            <h3 className="form-section-title">
              {block.title}
            </h3>
          )}

          {block.description && (
            <div className="form-section-description">
              {block.description}
            </div>
          )}

        </div>
      )}

      {block.children.map(render)}

    </section>
  )
}