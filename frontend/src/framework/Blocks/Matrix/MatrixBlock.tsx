// ============================================================
// src/framework/Blocks/Matrix/MatrixBlock.tsx
// ============================================================

import { CapabilityBoundary } from "@/framework/security/CapabilityBoundary"

import { useMatrix } from "./runtime/useMatrix"
import { MatrixGrid } from "./MatrixGrid"

type MatrixBlockType = {
  code: string
  params?: Record<string, unknown>
  context?: Record<string, unknown>
}

type Props = {
  block: MatrixBlockType
}


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
    block.params ?? block.context
  )

  if (loading) {
    return <div>Загрузка...</div>
  }

  if (!data) {
    return (
      <div>
        Не удалось загрузить матрицу
      </div>
    )
  }

  const canEdit =
    data.capabilities?.edit === true

  return (

    <CapabilityBoundary
      capabilities={
        data.capabilities
      }
    >

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 12,
        }}
      >

        <MatrixGrid
          layout={
            data.layout
          }

          cells={
            data.cells
          }

          schema={
            data.schema
          }
          onChange={
            canEdit
              ? updateCell
              : (() => {})

          }

        />

        {canEdit && (
          <div>
            <button
              type="button"
              onClick={() => {
                void submit()
              }}

              disabled={
                !dirty ||saving
              }
            >
              {saving
                ? "Сохранение..."
                : "Сохранить"}
            </button>
          </div>
        )}

        {error && (
          <div>
            {error}
          </div>

        )}
      </div>
    </CapabilityBoundary>
  )
}