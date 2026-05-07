import { api } from "@/framework/api/client"
import { useEffect, useState, useCallback } from "react"

export interface VisibleField {
  key: string
  label: string
  selected: boolean
}

interface MetaResponse {
  fields: {
    key: string
    label: string
    type: string
  }[]
  visible_fields: string[]
}

export function useVisibleFieldsRuntime(
  entity: string,
  fieldset: string,
  isOpen: boolean
) {
  const [fields, setFields] = useState<VisibleField[]>([])
  const [loading, setLoading] = useState(false)

  /* ---------- load ---------- */

  useEffect(() => {
    if (!isOpen) return

    let canceled = false

    const load = async () => {
      setLoading(true)

      try {
        const data = await api.get<MetaResponse>(
          `/entity/${entity}/meta/?fieldset=${fieldset}`
        )

        if (!canceled) {
          const normalized = data.fields
  .filter((f) => f.key) // ← защита от null
  .map((f) => ({
    key: f.key,
    label: f.label,
    selected: data.visible_fields.includes(f.key),
  }))

          setFields(normalized)
        }
      } finally {
        if (!canceled) setLoading(false)
      }
    }

    load()

    return () => {
      canceled = true
    }
  }, [isOpen, entity, fieldset])

  /* ---------- toggle ---------- */

  const toggleField = useCallback(
    (key: string, value: boolean) => {
      setFields((prev) =>
        prev.map((f) =>
          f.key === key ? { ...f, selected: value } : f
        )
      )
    },
    []
  )

  /* ---------- save ---------- */

  const save = useCallback(async () => {
    setLoading(true)

    try {
      const selectedKeys = fields
        .filter((f) => f.selected)
        .map((f) => f.key)

      await api.post(`/entity/${entity}/settings/`, {
        fields: selectedKeys,
      })
    } finally {
      setLoading(false)
    }
  }, [fields, entity])

  return {
    fields,
    loading,
    toggleField,
    save,
  }
}