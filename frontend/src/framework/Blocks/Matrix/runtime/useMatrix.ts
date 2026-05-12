import { useEffect, useRef, useState } from "react"
import { loadMatrix } from "@/framework/api/matrix/loadMatrix"
import { buildMatrixChanges } from "./matrixDiff"
import { getCellKey } from "./matrixKey"
import { useMatrixAutosave } from "./useMatrixAutosave"
import { submitMatrix } from "@/framework/api/matrix/submitMatrix"
import type { MatrixCellValue, MatrixData } from "../types"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import { resolveObject } from "@/framework/bind/expression/resolveUnified"

// 🔥 ДОБАВИЛИ

export function useMatrix(
  code: string,
  context?: Record<string, unknown>
) {
  // 🔥 runtime DSL context
  const runtimeCtx = usePageRuntimeContext()

  // 🔥 RESOLVE DSL → реальные значения
  const resolvedContext = context
    ? resolveObject(context, runtimeCtx)
    : context

  console.log("🔥 MATRIX RAW:", context)
  console.log("🔥 MATRIX RESOLVED:", resolvedContext)

  const [data, setData] = useState<MatrixData | null>(null)

  const initialRef = useRef<Record<string, MatrixCellValue>>({})

  // 🔥 ВАЖНО: зависимость от resolved, а не raw
  const ctxKey = JSON.stringify(resolvedContext ?? {})

  // =========================
  // LOAD
  // =========================
  useEffect(() => {
    loadMatrix(code, resolvedContext).then(res => {
      setData(res)
      initialRef.current = res.cells || {}
    })
  }, [code, ctxKey])

  // =========================
  // AUTOSAVE
  // =========================
  useMatrixAutosave({
    code,
    data,
    initialRef,
  })

  // =========================
  // UPDATE CELL
  // =========================
  const updateCell = (
    x: string,
    y: string,
    patch: Partial<MatrixCellValue>
  ) => {
    setData(prev => {
      if (!prev) return prev

      const key = getCellKey(x, y)
      const current = prev.cells[key] || {}

      return {
        ...prev,
        cells: {
          ...prev.cells,
          [key]: {
            ...current,
            ...patch,
          },
        },
      }
    })
  }

  // =========================
  // MANUAL SUBMIT
  // =========================
  const submit = async () => {
    if (!data) return

    const changes = buildMatrixChanges(
      data.cells,
      initialRef.current
    )

    if (!changes.length) return

    await submitMatrix(code, changes)
    initialRef.current = data.cells
  }

  return {
    data,
    updateCell,
    submit,
  }
}