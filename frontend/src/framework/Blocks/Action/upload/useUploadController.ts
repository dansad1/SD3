// src/framework/Blocks/Action/upload/useUploadController.ts

import {
  useMemo,
  useState,
} from "react"

import {
  usePageRuntimeContext,
} from "@/framework/page/runtime/usePageRuntimeContext"

import {
  commitFiles,
  discardFiles,
  uploadFile,
} from "@/framework/api/uploadApi"

import {
  resolveUploadCtx,
} from "./uploadCtx"

import type {
  UploadActionResult,
  UploadBlock,
  UploadRuntimeItem,
  UploadTempItem,
} from "./types"


function getErrorMessage(
  error: unknown,
): string {
  if (
    error instanceof Error
    && error.message
  ) {
    return error.message
  }

  return "Не удалось выполнить загрузку"
}


function isRecord(
  value: unknown,
): value is Record<string, unknown> {
  return (
    typeof value === "object"
    && value !== null
    && !Array.isArray(value)
  )
}


function isUploadTempItem(
  value: unknown,
): value is UploadTempItem {
  if (!isRecord(value)) {
    return false
  }

  return (
    typeof value.id === "number"
    && typeof value.name === "string"
  )
}


function extractFiles(
  result: UploadActionResult,
  resultKey?: string,
): UploadTempItem[] {
  if (!resultKey) {
    return []
  }

  const value = result[resultKey]

  if (!Array.isArray(value)) {
    throw new Error(
      `Action не вернул массив "${resultKey}"`,
    )
  }

  if (!value.every(isUploadTempItem)) {
    throw new Error(
      `Некорректный формат файлов в "${resultKey}"`,
    )
  }

  return value
}


export function useUploadController(
  block: UploadBlock,
) {
  const runtimeContext =
    usePageRuntimeContext() as Record<
      string,
      unknown
    >

  const [
    runtime,
    setRuntime,
  ] = useState<UploadRuntimeItem[]>([])

  const [
    tempFiles,
    setTempFiles,
  ] = useState<UploadTempItem[]>(
    block.files ?? [],
  )

  /*
   * Универсальный результат последнего multipart action.
   *
   * Контроллер ничего не знает о rows, preview,
   * пользователях или импорте.
   */
  const [
    result,
    setResult,
  ] = useState<UploadActionResult | null>(
    null,
  )

  const [
    committing,
    setCommitting,
  ] = useState(false)

  const [
    discardingIds,
    setDiscardingIds,
  ] = useState<Set<number>>(
    () => new Set(),
  )

  const resolvedCtx = useMemo(
    () =>
      resolveUploadCtx(
        block.ctx,
        runtimeContext,
      ),
    [
      block.ctx,
      runtimeContext,
    ],
  )

  const uploading = runtime.some(
    item =>
      item.status === "uploading",
  )

  function setProgress(
    localId: string,
    progress: number,
  ): void {
    const safeProgress = Math.max(
      0,
      Math.min(
        progress,
        100,
      ),
    )

    setRuntime(previous =>
      previous.map(item =>
        item.localId === localId
          ? {
              ...item,
              progress: safeProgress,
            }
          : item,
      ),
    )
  }

  function setError(
    localId: string,
    error: unknown,
  ): void {
    setRuntime(previous =>
      previous.map(item =>
        item.localId === localId
          ? {
              ...item,
              status: "error",
              error: getErrorMessage(
                error,
              ),
            }
          : item,
      ),
    )
  }

  function removeRuntime(
    localId: string,
  ): void {
    setRuntime(previous =>
      previous.filter(
        item =>
          item.localId !== localId,
      ),
    )
  }

  function appendFiles(
    files: UploadTempItem[],
  ): void {
    if (files.length === 0) {
      return
    }

    setTempFiles(previous => {
      if (!block.multiple) {
        return [
          files[0],
        ]
      }

      const existingIds = new Set(
        previous.map(
          item => item.id,
        ),
      )

      const uniqueFiles =
        files.filter(
          item =>
            !existingIds.has(
              item.id,
            ),
        )

      return [
        ...previous,
        ...uniqueFiles,
      ]
    })
  }

  async function uploadOne(
    file: File,
  ): Promise<void> {
    if (block.disabled) {
      return
    }

    const localId =
      crypto.randomUUID()

    setRuntime(previous => [
      ...previous,
      {
        localId,
        name: file.name,
        progress: 0,
        status: "uploading",
      },
    ])

    try {
      const actionResult =
        await uploadFile(
          block.upload_action,
          file,
          resolvedCtx,
          progress =>
            setProgress(
              localId,
              progress,
            ),
        )

      /*
       * Сохраняем весь ответ.
       * Никаких знаний о структуре конкретного action.
       */
      setResult(
        actionResult,
      )

      const uploadedFiles =
        extractFiles(
          actionResult,
          block.result_key,
        )

      /*
       * Commit имеет смысл только для файлового ответа.
       */
      if (
        block.auto_commit
        && uploadedFiles.length > 0
      ) {
        if (!block.commit_action) {
          throw new Error(
            "Для auto_commit не задан commit_action",
          )
        }

        await commitFiles(
          block.commit_action,
          uploadedFiles.map(
            item => item.id,
          ),
          resolvedCtx,
        )
      }

      appendFiles(
        uploadedFiles,
      )

      /*
       * Удаляем строку прогресса только после
       * полного успешного выполнения.
       */
      removeRuntime(
        localId,
      )
    } catch (error) {
      console.error(
        "Upload failed",
        error,
      )

      setError(
        localId,
        error,
      )
    }
  }

  async function uploadMany(
    files: File[],
  ): Promise<void> {
    if (
      block.disabled
      || files.length === 0
    ) {
      return
    }

    const selectedFiles =
      block.multiple
        ? files
        : files.slice(
            0,
            1,
          )

    await Promise.all(
      selectedFiles.map(
        file =>
          uploadOne(
            file,
          ),
      ),
    )
  }

  async function discardOne(
    id: number,
  ): Promise<void> {
    if (
      block.disabled
      || discardingIds.has(id)
    ) {
      return
    }

    const discardAction =
      block.discard_action
      ?? block.commit_action

    if (!discardAction) {
      console.error(
        "Discard action is not configured",
      )

      return
    }

    setDiscardingIds(previous => {
      const next = new Set(
        previous,
      )

      next.add(
        id,
      )

      return next
    })

    try {
      await discardFiles(
        discardAction,
        [id],
        resolvedCtx,
      )

      setTempFiles(previous =>
        previous.filter(
          item =>
            item.id !== id,
        ),
      )
    } catch (error) {
      console.error(
        "Discard failed",
        error,
      )
    } finally {
      setDiscardingIds(previous => {
        const next = new Set(
          previous,
        )

        next.delete(
          id,
        )

        return next
      })
    }
  }

  async function commitAll(): Promise<void> {
    if (
      block.disabled
      || block.auto_commit
      || committing
    ) {
      return
    }

    if (!block.commit_action) {
      console.error(
        "Commit action is not configured",
      )

      return
    }

    const ids = tempFiles.map(
      item => item.id,
    )

    if (ids.length === 0) {
      return
    }

    setCommitting(
      true,
    )

    try {
      await commitFiles(
        block.commit_action,
        ids,
        resolvedCtx,
      )

      setTempFiles([])
    } catch (error) {
      console.error(
        "Commit failed",
        error,
      )
    } finally {
      setCommitting(
        false,
      )
    }
  }

  return {
    runtime,
    tempFiles,
    result,

    uploading,
    committing,
    discardingIds,

    uploadMany,
    discardOne,
    commitAll,
    removeRuntime,

    disabled:
      block.disabled
      ?? false,
  }
}