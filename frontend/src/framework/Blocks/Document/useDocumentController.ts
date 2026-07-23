import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react"

import { submitAction } from "@/framework/api/action/submitAction"

import type {
  DocumentBlock,
  DocumentVM,
} from "./types"

type OpenDocumentResponse = {
  document?: {
    content?: unknown
  }
}

function buildObjectPayload(
  objectId: string | undefined
): Record<string, string> {
  if (!objectId) {
    return {}
  }

  return {
    id: objectId,
  }
}

function getErrorMessage(error: unknown): string {
  if (error instanceof Error) {
    return error.message
  }

  return "Не удалось выполнить операцию"
}

export function useDocumentController(
  block: DocumentBlock
): DocumentVM {
  const [saving, setSaving] = useState(false)
  const [content, setContentState] = useState("")
  const [error, setError] = useState<string | null>(null)
  const [loadedKey, setLoadedKey] = useState<string | null>(null)

  const requestIdRef = useRef(0)
  const hydratedRef = useRef(false)
  const lastSavedContentRef = useRef("")

  const mode = useMemo(() => {
    if (block.mode) {
      return block.mode
    }

    return block.editable === false
      ? "read"
      : "edit"
  }, [
    block.editable,
    block.mode,
  ])

  const editable =
    mode === "edit" &&
    Boolean(block.saveAction)

  const documentKey = useMemo(() => {
    return JSON.stringify({
      action: block.openAction,
      objectId: block.objectId ?? null,
      ctx: block.ctx ?? null,
    })
  }, [
    block.ctx,
    block.objectId,
    block.openAction,
  ])

  const loading = loadedKey !== documentKey

  /*
   * OPEN
   */

  useEffect(() => {
    const requestId = requestIdRef.current + 1

    requestIdRef.current = requestId
    hydratedRef.current = false

    const openDocument = async (): Promise<void> => {
      try {
        const response = await submitAction(
          block.openAction,
          buildObjectPayload(block.objectId),
          block.ctx
        ) as OpenDocumentResponse

        if (requestId !== requestIdRef.current) {
          return
        }

        const document = response.document

        const nextContent =
          document &&
          typeof document === "object" &&
          "content" in document
            ? String(document.content ?? "")
            : ""

        setContentState(nextContent)
        lastSavedContentRef.current = nextContent
        setError(null)
      } catch (openError: unknown) {
        if (requestId !== requestIdRef.current) {
          return
        }

        setContentState("")
        setError(getErrorMessage(openError))
      } finally {
        if (requestId === requestIdRef.current) {
          hydratedRef.current = true
          setLoadedKey(documentKey)
        }
      }
    }

    void openDocument()

    return () => {
      requestIdRef.current += 1
    }
  }, [
    block.ctx,
    block.objectId,
    block.openAction,
    documentKey,
  ])

  /*
   * CHANGE
   */

  const setContent = useCallback((value: string): void => {
    setContentState(value)
    setError(null)
  }, [])

  /*
   * SAVE
   */

  const save = useCallback(async (): Promise<void> => {
    if (!block.saveAction) {
      return
    }

    if (mode !== "edit") {
      return
    }

    if (content === lastSavedContentRef.current) {
      return
    }

    setSaving(true)
    setError(null)

    try {
      await submitAction(
        block.saveAction,
        {
          ...buildObjectPayload(block.objectId),
          content,
        },
        block.ctx
      )

      lastSavedContentRef.current = content
    } catch (saveError: unknown) {
      setError(getErrorMessage(saveError))

      throw saveError
    } finally {
      setSaving(false)
    }
  }, [
    block.ctx,
    block.objectId,
    block.saveAction,
    content,
    mode,
  ])

  /*
   * AUTOSAVE
   */

  useEffect(() => {
    if (!hydratedRef.current) {
      return
    }

    if (!block.autosave) {
      return
    }

    if (!block.saveAction) {
      return
    }

    if (mode !== "edit") {
      return
    }

    if (content === lastSavedContentRef.current) {
      return
    }

    const timeoutId = window.setTimeout(() => {
      void save().catch(() => {
        /*
         * Ошибка уже записана в error.
         */
      })
    }, block.autosaveDelay ?? 1000)

    return () => {
      window.clearTimeout(timeoutId)
    }
  }, [
    block.autosave,
    block.autosaveDelay,
    block.saveAction,
    content,
    mode,
    save,
  ])

  return {
    loading,
    saving,
    error,

    content,

    mode,
    editable,

    toolbar: block.toolbar ?? "full",
    fullscreen: Boolean(block.fullscreen),

    setContent,
    save,
  }
}