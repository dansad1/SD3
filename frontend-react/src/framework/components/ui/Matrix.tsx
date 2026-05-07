// framework/ui/Matrix.tsx

import type {
  MatrixDefinition,
  MatrixLayout,
} from "../../Blocks/Matrix/types/types"

interface Props {
  definition: MatrixDefinition
  layout?: MatrixLayout
  editable?: boolean

  isLoading?: boolean
  isEmpty?: boolean
  emptyMessage?: string

  children: React.ReactNode
}

export function Matrix({
  definition,
  layout = "grid",
  editable = true,

  isLoading = false,
  isEmpty = false,
  emptyMessage = "Нет данных",

  children,
}: Props) {
  const className = [
    "ui-matrix",
    `ui-matrix--${definition.cell.type}`,
    `ui-matrix--layout-${layout}`,
    editable ? "ui-matrix--editable" : "ui-matrix--readonly",
  ]
    .filter(Boolean)
    .join(" ")

  return (
    <div className="ui-matrix-wrapper">
      <div className={className}>
        <div className="ui-matrix-content">
          {children}
        </div>

        {isLoading && (
          <div className="ui-matrix-loading-overlay">
            Загрузка…
          </div>
        )}

        {isEmpty && !isLoading && (
          <div className="ui-matrix-empty">
            {emptyMessage}
          </div>
        )}
      </div>
    </div>
  )
}