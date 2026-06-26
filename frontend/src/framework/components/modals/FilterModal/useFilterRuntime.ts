import {
  useCallback,
  useEffect,
  useState,
} from "react"

import type {
  FieldSchema,
  Value,
} from "../../dynamic/types"

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
  saved_filters?: SavedFilter[]
}

/* ---------- helpers ---------- */

function isBooleanField(field: FieldSchema): boolean {
  return (
    field.widget === "checkbox" ||
    field.widget === "boolean" ||
    field.html_type === "checkbox"
  )
}

/* ---------- hook ---------- */

export function useFilterRuntime(
  entity: string,
  fieldset: string,
  initialQuery: Record<string, string | string[]> = {},
) {
  const [loading, setLoading] = useState(false)
  const [fields, setFields] = useState<FieldSchema[]>([])
  const [savedFilters, setSavedFilters] = useState<SavedFilter[]>([])
  const [values, setValues] = useState<Record<string, Value>>({})

  const buildEmptyValues = useCallback(
    (items: FieldSchema[]) => {
      const next: Record<string, Value> = {}

      for (const field of items) {
        if (field.multiple) {
          next[field.name] = []
        } else if (isBooleanField(field)) {
          next[field.name] = false
        } else {
          next[field.name] = ""
        }
      }

      return next
    },
    [],
  )

  const applyQueryToValues = useCallback(
    (
      items: FieldSchema[],
      query: Record<string, string | string[]>,
    ) => {
      const next = buildEmptyValues(items)

      for (const field of items) {
        const raw = query[field.name]

        if (raw === undefined) {
          continue
        }

        if (field.multiple) {
          next[field.name] = Array.isArray(raw)
            ? raw
            : String(raw).split(",")
        } else if (isBooleanField(field)) {
          const value = Array.isArray(raw)
            ? raw[0]
            : raw

          next[field.name] = (
            value === "1" ||
            value === "true" ||
            value === "on"
          )
        } else {
          next[field.name] = Array.isArray(raw)
            ? raw[0]
            : raw
        }
      }

      return next
    },
    [buildEmptyValues],
  )

  useEffect(() => {
    let canceled = false

    async function load() {
      try {
        setLoading(true)

        const data = await api.get<FilterMetaResponse>(
          `/entity/${entity}/filter/meta/?fieldset=${fieldset}`,
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
            initialQuery,
          ),
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

    // ВАЖНО:
    // initialQuery специально не добавляем.
    // Иначе {} из FilterModal создаёт бесконечные запросы.
  }, [
    entity,
    fieldset,
    applyQueryToValues,
  ])

  const setFieldValue = useCallback(
    (name: string, value: Value) => {
      setValues(prev => ({
        ...prev,
        [name]: value,
      }))
    },
    [],
  )

  const buildQuery = useCallback(() => {
    const query: Record<string, string> = {}

    for (const field of fields) {
      const value = values[field.name]

      if (Array.isArray(value)) {
        if (value.length > 0) {
          query[field.name] = value.join(",")
        }

        continue
      }

      if (
        typeof value === "string" &&
        value.trim()
      ) {
        query[field.name] = value
        continue
      }

      if (typeof value === "boolean") {
        if (value) {
          query[field.name] = "1"
        }
      }
    }

    return query
  }, [
    fields,
    values,
  ])

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