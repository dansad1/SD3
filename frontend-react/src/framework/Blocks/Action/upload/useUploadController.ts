import { useMemo, useState } from "react"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import { resolveUploadCtx } from "./uploadCtx"
import { commitFiles, discardFiles, uploadFile,  } from "@/framework/api/uploadApi"
import type { UploadBlock, UploadTempItem } from "./types"


type RuntimeItem = {
  localId: string
  name: string
  progress: number
  status: "uploading" | "error"
}

export function useUploadController(block: UploadBlock) {
  const runtimeContext =
    usePageRuntimeContext() as Record<string, unknown>

  const [runtime, setRuntime] = useState<RuntimeItem[]>([])
  const [tempFiles, setTempFiles] = useState<UploadTempItem[]>(
    block.files ?? []
  )

  const resolvedCtx = useMemo(
    () => resolveUploadCtx(block.ctx, runtimeContext),
    [block.ctx, runtimeContext]
  )

  const setProgress = (localId: string, progress: number) => {
    setRuntime(prev =>
      prev.map(x =>
        x.localId === localId ? { ...x, progress } : x
      )
    )
  }

  const setError = (localId: string) => {
    setRuntime(prev =>
      prev.map(x =>
        x.localId === localId ? { ...x, status: "error" } : x
      )
    )
  }

  const removeRuntime = (localId: string) => {
    setRuntime(prev => prev.filter(x => x.localId !== localId))
  }

  const uploadOne = async (file: File) => {
    const localId = crypto.randomUUID()

    setRuntime(prev => [
      ...prev,
      {
        localId,
        name: file.name,
        progress: 0,
        status: "uploading",
      },
    ])

    try {
      const files = await uploadFile(
        block.upload_action,
        file,
        resolvedCtx,
        percent => setProgress(localId, percent)
      )

      removeRuntime(localId)

      setTempFiles(prev => [...prev, ...files])

      if (block.auto_commit) {
        await commitFiles(
          block.commit_action,
          files.map(f => f.id),
          resolvedCtx
        )

        setTempFiles(prev =>
          prev.filter(
            f => !files.some(x => x.id === f.id)
          )
        )
      }
    } catch (e) {
      console.error("upload failed", e)
      setError(localId)
    }
  }

  const uploadMany = (files: File[]) => {
    if (block.disabled) return
    files.forEach(uploadOne)
  }

  const discardOne = async (id: number) => {
    try {
      await discardFiles(block.commit_action, [id], resolvedCtx)

      setTempFiles(prev => prev.filter(f => f.id !== id))
    } catch (e) {
      console.error("discard failed", e)
    }
  }

  const commitAll = async () => {
    const ids = tempFiles.map(f => f.id)
    if (!ids.length) return

    try {
      await commitFiles(block.commit_action, ids, resolvedCtx)
      setTempFiles([])
    } catch (e) {
      console.error("commit failed", e)
    }
  }

  return {
    runtime,
    tempFiles,
    uploadMany,
    discardOne,
    commitAll,
    disabled: block.disabled,
  }
}