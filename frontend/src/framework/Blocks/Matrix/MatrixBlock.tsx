// ============================================================
// src/framework/Blocks/Matrix/MatrixBlock.tsx
// ============================================================

import {
  CapabilityBoundary,
} from "@/framework/security/CapabilityBoundary"

import {
  MatrixGrid,
} from "./MatrixGrid"

import {
  useMatrix,
} from "./runtime/useMatrix"


type MatrixBlockType = {
  code: string
  params?: Record<string, unknown>
  context?: Record<string, unknown>
}


type Props = {
  block: MatrixBlockType
}


const readonlyChangeHandler = () => undefined


export const MatrixBlock = ({
  block,
}: Props) => {
  const {
    data,
    loading,
    saving,
    error,
    dirty,
    updateCell,
    submit,
  } = useMatrix(
    block.code,
    block.params ?? block.context,
  )

  if (loading) {
    return (
      <div className="ui-matrix-loading">
        Загрузка матрицы...
      </div>
    )
  }

  if (!data) {
    return (
      <div className="ui-matrix-empty">
        Не удалось загрузить матрицу
      </div>
    )
  }

  const canEdit =
    data.capabilities?.edit === true

  const handleChange = canEdit
    ? updateCell
    : readonlyChangeHandler

  return (
    <CapabilityBoundary
      capabilities={data.capabilities}
    >
      <div className="matrix-block">
        {error && (
          <div
            className="matrix-block__error"
            role="alert"
          >
            {error}
          </div>
        )}

        <MatrixGrid
          layout={data.layout}
          cells={data.cells}
          schema={data.schema}
          onChange={handleChange}
        />

        {canEdit && (
          <footer className="matrix-block__actions">
            <span className="matrix-block__state">
              {saving
                ? "Сохранение..."
                : dirty
                  ? "Есть несохранённые изменения"
                  : "Изменения сохранены"}
            </span>

            <button
              type="button"
              className={
                "ui-btn ui-btn-primary ui-btn-sm"
                + (
                  saving
                    ? " is-loading"
                    : ""
                )
              }
              disabled={!dirty || saving}
              onClick={() => {
                void submit()
              }}
            >
              {saving
                ? "Сохранение..."
                : "Сохранить"}
            </button>
          </footer>
        )}
      </div>
    </CapabilityBoundary>
  )
}