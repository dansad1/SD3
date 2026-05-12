// SectionBlock.tsx

import type { BlockComponent } from "../Registry/BlockRegistry"

export const SectionBlock: BlockComponent<"section"> = ({
  block,
  children,
}) => {
  return (
    <section className="ui-section">

      {(block.title || block.description) && (
        <div className="ui-section-header">

          {block.title && (
            <h2 className="ui-section-title">
              {block.title}
            </h2>
          )}

          {block.description && (
            <p className="ui-muted">
              {block.description}
            </p>
          )}

        </div>
      )}

      <div className="ui-section-body">
        {children}
      </div>

    </section>
  )
}