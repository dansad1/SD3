import { useEffect, useRef } from "react"
import { buildMatrixChanges } from "./matrixDiff"
import { submitMatrix } from "@/framework/api/matrix/submitMatrix"
import type { MatrixCellValue, MatrixData } from "../types"

type Params = {
  code: string
  data: MatrixData | null
  initialRef: React.MutableRefObject<Record<string, MatrixCellValue>>
}

export function useMatrixAutosave({ code, data, initialRef }: Params) {
  const latestDataRef = useRef<MatrixData | null>(null)
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const isInitialLoad = useRef(true)

  // sync latest
  useEffect(() => {
    latestDataRef.current = data
  }, [data])

  const scheduleSave = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
    }

    timeoutRef.current = setTimeout(async () => {
      const currentData = latestDataRef.current
      if (!currentData) return

      const changes = buildMatrixChanges(
        currentData.cells,
        initialRef.current
      )

      if (!changes.length) return

      await submitMatrix(code, changes)

      initialRef.current = currentData.cells
    }, 500)
  }

  // trigger
  useEffect(() => {
    if (!data) return

    if (isInitialLoad.current) {
      isInitialLoad.current = false
      return
    }

    scheduleSave()
  }, [data])

  // cleanup
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])
}