// useDocumentController.ts

import { useCallback, useEffect, useState } from "react"


import type {
  DocumentBlock,
  DocumentVM,
} from "./types"
import { submitAction } from "@/framework/api/action/submitAction"

export function useDocumentController(
  block: DocumentBlock
): DocumentVM {

  const [loading, setLoading] = useState(true)

  const [saving, setSaving] = useState(false)

  const [content, setContent] = useState("")

  /*
   * OPEN
   */

  useEffect(() => {

    setLoading(true)

    submitAction(
      block.openAction,
      {
        id: block.objectId,
      },
      block.ctx
    )
      .then(res => {

        const html =
          typeof res.document === "object" &&
          res.document &&
          "content" in res.document
            ? String(res.document.content || "")
            : ""

        setContent(html)
      })
      .finally(() => {
        setLoading(false)
      })

  }, [
    block.objectId,
    block.openAction,
    block.ctx,
  ])

  /*
   * SAVE
   */

  const save = useCallback(async () => {

    if (!block.saveAction) {
      return
    }

    setSaving(true)

    try {

      await submitAction(
        block.saveAction,
        {
          id: block.objectId,
          content,
        },
        block.ctx
      )

    } finally {

      setSaving(false)

    }

  }, [
    block.saveAction,
    block.objectId,
    block.ctx,
    content,
  ])

  /*
   * AUTOSAVE
   */

  useEffect(() => {

    if (!block.autosave) {
      return
    }

    if (!block.saveAction) {
      return
    }

    const timeout = setTimeout(() => {
      save()
    }, block.autosaveDelay || 1000)

    return () => {
      clearTimeout(timeout)
    }

  }, [
    content,
    block.autosave,
    block.autosaveDelay,
    block.saveAction,
    save,
  ])

  return {
    loading,
    saving,

    content,

    editable: block.editable ?? true,

    toolbar: block.toolbar || "full",

    fullscreen: !!block.fullscreen,

    setContent,

    save,
  }
}