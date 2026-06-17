import { useCallback, useEffect, useState } from "react"

import { loadMatrix } from "@/framework/api/matrix/loadMatrix"
import { submitMatrix } from "@/framework/api/matrix/submitMatrix"

import { buildMatrixChanges } from "./matrixDiff"
import { getCellKey } from "./matrixKey"

import type {
  MatrixCellValue,
  MatrixData,
} from "../types"

import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import { resolveObject } from "@/framework/bind/expression/resolveUnified"

export function useMatrix(
  code: string,
  context?: Record<string, unknown>
) {
  const runtimeCtx =
    usePageRuntimeContext()

  const resolvedContext = context
    ? resolveObject(
        context,
        runtimeCtx
      )
    : context

  const [data, setData] =
    useState<MatrixData | null>(null)

  const [initialCells, setInitialCells] =
    useState<
      Record<
        string,
        MatrixCellValue
      >
    >({})

  const [loading, setLoading] =
    useState(true)

  const [saving, setSaving] =
    useState(false)

  const [error, setError] =
    useState<string | null>(
      null
    )

  const ctxKey = JSON.stringify(
    resolvedContext ?? {}
  )

  // =========================
  // LOAD
  // =========================

  const reload = useCallback(
    async () => {
      setLoading(true)
      setError(null)

      try {
        const res =
          await loadMatrix(
            code,
            resolvedContext
          )

        setData(res)

        setInitialCells(
          res.cells || {}
        )
      } catch (e) {
        setError(
          e instanceof Error
            ? e.message
            : "Ошибка загрузки"
        )
      } finally {
        setLoading(false)
      }
    },
    [code, ctxKey]
  )

  useEffect(() => {
    let cancelled = false

    async function run() {
      setLoading(true)
      setError(null)

      try {
        const res =
          await loadMatrix(
            code,
            resolvedContext
          )

        if (cancelled) {
          return
        }

        setData(res)

        setInitialCells(
          res.cells || {}
        )
      } catch (e) {
        if (cancelled) {
          return
        }

        setError(
          e instanceof Error
            ? e.message
            : "Ошибка загрузки"
        )
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    void run()

    return () => {
      cancelled = true
    }
  }, [code, ctxKey])

  // =========================
  // UPDATE CELL
  // =========================

  const updateCell = (
    x: string,
    y: string,
    patch: Partial<MatrixCellValue>
  ) => {
    setData(prev => {
      if (!prev) {
        return prev
      }

      const key =
        getCellKey(x, y)

      const current =
        prev.cells[key] || {}

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
  // DIRTY
  // =========================

  const dirty =
    data != null &&
    buildMatrixChanges(
      data.cells,
      initialCells
    ).length > 0

  // =========================
  // SAVE
  // =========================

 const submit =
  async () => {

    if (!data) {
      return
    }

    const changes =

      buildMatrixChanges(

        data.cells,

        initialCells,

      )

    if (

      changes.length === 0

    ) {

      return

    }

    setSaving(true)

    setError(null)

    try {

      await submitMatrix(

        code,

        changes,

        resolvedContext,

      )

      setInitialCells({

        ...data.cells,

      })

    }

    catch (e) {

      setError(

        e instanceof Error

          ? e.message

          : "Ошибка сохранения"

      )

      throw e

    }

    finally {

      setSaving(false)

    }

  }
    async () => {
      if (!data) {
        return
      }

      const changes =
        buildMatrixChanges(
          data.cells,
          initialCells
        )

      if (
        changes.length === 0
      ) {
        return
      }

      setSaving(true)
      setError(null)

      try {
        await submitMatrix(
          code,
          changes
        )

        setInitialCells({
          ...data.cells,
        })
      } catch (e) {
        setError(
          e instanceof Error
            ? e.message
            : "Ошибка сохранения"
        )

        throw e
      } finally {
        setSaving(false)
      }
    }

  return {
    data,

    loading,
    saving,

    error,

    dirty,

    updateCell,

    submit,

    reload,
  }
}