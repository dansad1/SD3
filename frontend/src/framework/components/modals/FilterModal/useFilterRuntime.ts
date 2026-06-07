import { useEffect, useState, useCallback } from "react"
import type { FieldSchema, Value } from "../../dynamic/types"
import { api } from "@/framework/api/client"
import { validateFieldSchema } from "../../dynamic/validateSchema"

/* ---------- types ---------- */

export interface SavedFilter {
  id: number
  name: string
  query: Record<string, string | string[]>
}

interface FilterMetaResponse {
  fields: FieldSchema[]
  saved_filters: SavedFilter[]
}

/* ---------- helpers ---------- */

function isBooleanField(field: FieldSchema): boolean {
  return (
    field.widget === "checkbox" ||
    field.html_type === "checkbox"
  )
}

/* ---------- hook ---------- */

export function useFilterRuntime(
  entity: string,
  fieldset: string,
  initialQuery: Record<string, string | string[]>
) {
  const [loading, setLoading] = useState(true)
  const [fields, setFields] = useState<FieldSchema[]>([])
  const [savedFilters, setSavedFilters] = useState<SavedFilter[]>([])
  const [values, setValues] = useState<Record<string, Value>>({})

  /* ---------- helpers ---------- */

  const buildEmptyValues = useCallback(
    (fields: FieldSchema[]) => {
      const v: Record<string, Value> = {}

      for (const f of fields) {
        if (f.multiple) {
          v[f.name] = []
        } else if (isBooleanField(f)) {
          v[f.name] = false
        } else {
          v[f.name] = ""
        }
      }

      return v
    },
    []
  )

  const applyQueryToValues = useCallback(
    (
      fields: FieldSchema[],
      query: Record<string, string | string[]>
    ) => {
      const v = buildEmptyValues(fields)

      for (const f of fields) {
        const key = `field_${f.id}`
        const raw = query[key]

        if (raw === undefined) {
          continue
        }

        if (f.multiple) {
          v[f.name] = Array.isArray(raw)
            ? raw
            : String(raw).split(",")
        } else if (isBooleanField(f)) {
          const value = Array.isArray(raw)
            ? raw[0]
            : raw

          v[f.name] =
            value === "1" ||
            value === "true" ||
            value === "on"
        } else {
          v[f.name] = Array.isArray(raw)
            ? raw[0]
            : raw
        }
      }

      return v
    },
    [buildEmptyValues]
  )

  /* ---------- load meta ---------- */

  useEffect(() => {
    let canceled = false

    const load = async () => {
      try {
        setLoading(true)

        const data =
          await api.get<FilterMetaResponse>(
            `/${entity}/filter/meta/?fieldset=${fieldset}`
          )

        if (canceled) {
          return
        }

        data.fields.forEach(validateFieldSchema)

        setFields(data.fields)
        setSavedFilters(data.saved_filters ?? [])

        setValues(
          applyQueryToValues(
            data.fields,
            initialQuery
          )
        )
      } finally {
        if (!canceled) {
          setLoading(false)
        }
      }
    }

    void load()

    return () => {
      canceled = true
    }
  }, [
    entity,
    fieldset,
    initialQuery,
    applyQueryToValues,
  ])

  /* ---------- public actions ---------- */

  const setFieldValue = useCallback(
    (name: string, value: Value) => {
      setValues(prev => ({
        ...prev,
        [name]: value,
      }))
    },
    []
  )

  const buildQuery = useCallback(() => {
    const q: Record<string, string> = {}

    for (const f of fields) {
      const val = values[f.name]
      const key = `field_${f.id}`

      if (Array.isArray(val) && val.length > 0) {
        q[key] = val.join(",")
      } else if (
        typeof val === "string" &&
        val.trim()
      ) {
        q[key] = val
      } else if (typeof val === "boolean") {
        q[key] = val ? "1" : "0"
      }
    }

    return q
  }, [fields, values])

  /* ---------- export ---------- */

  return {
    loading,
    fields,
    values,
    savedFilters,

    setFieldValue,
    setValues,
    setSavedFilters,

    buildEmptyValues,
    buildQuery,
  }
}