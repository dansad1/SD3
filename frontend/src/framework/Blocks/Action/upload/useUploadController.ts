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

  return "Не удалось загрузить файл"
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
              error:
                getErrorMessage(error),
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
    if (!files.length) {
      return
    }

    setTempFiles(previous => {
      if (!block.multiple) {
        return [
          files[0],
        ]
      }

      const existingIds =
        new Set(
          previous.map(
            item => item.id,
          ),
        )

      const uniqueFiles =
        files.filter(
          item =>
            !existingIds.has(item.id),
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
      const uploaded =
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

      removeRuntime(localId)

      if (!uploaded.length) {
        return
      }

      if (block.auto_commit) {
        await commitFiles(
          block.commit_action,
          uploaded.map(
            item => item.id,
          ),
          resolvedCtx,
        )
      }

      appendFiles(uploaded)
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
      || !files.length
    ) {
      return
    }

    const selectedFiles =
      block.multiple
        ? files
        : files.slice(0, 1)

    await Promise.all(
      selectedFiles.map(
        file => uploadOne(file),
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

    setDiscardingIds(previous => {
      const next = new Set(previous)

      next.add(id)

      return next
    })

    try {
      await discardFiles(
        block.commit_action,
        [id],
        resolvedCtx,
      )

      setTempFiles(previous =>
        previous.filter(
          item => item.id !== id,
        ),
      )
    } catch (error) {
      console.error(
        "Discard failed",
        error,
      )
    } finally {
      setDiscardingIds(previous => {
        const next = new Set(previous)

        next.delete(id)

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

    const ids = tempFiles.map(
      item => item.id,
    )

    if (!ids.length) {
      return
    }

    setCommitting(true)

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
      setCommitting(false)
    }
  }

  return {
    runtime,
    tempFiles,
    uploading,
    committing,
    discardingIds,

    uploadMany,
    discardOne,
    commitAll,
    removeRuntime,

    disabled:
      block.disabled ?? false,
  }
}