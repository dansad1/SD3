import {
  useCallback,
  useRef,
  useState,
  useEffect,
  useMemo,
} from "react"

import type { Json } from "@/framework/types/json"
import type { FormSchema } from "../../types/types"
import type {
  FormRuntimeMeta,
  FormRuntimeState,
} from "../reactions/types"

/* ================= TYPES ================= */

export type FormState = ReturnType<
  typeof useFormState<FormSchema>
>

type Primitive = string | number | boolean | null

type RelationObject = {
  value?: Primitive
  id?: Primitive
}

/* ================= HELPERS ================= */

function normalizeValue(value: Json): Json {
  if (Array.isArray(value)) {
    return value
      .map(v => {
        if (typeof v === "object" && v !== null) {
          const obj = v as RelationObject

          if (obj.value !== undefined) return obj.value
          if (obj.id !== undefined) return obj.id

          return null
        }

        return v
      })
      .filter((v): v is Primitive => v !== null)
  }

  if (typeof value === "object" && value !== null) {
    const obj = value as RelationObject

    if (obj.value !== undefined) return obj.value
    if (obj.id !== undefined) return obj.id

    return null
  }

  return value
}

function createMeta(): FormRuntimeMeta {
  return {
    visible: {},
    disabled: {},
  }
}

/* ================= HOOK ================= */

export function useFormState<Schema>() {
  const [schema, setSchema] = useState<Schema | null>(null)

  const [values, setValues] = useState<Record<string, Json>>({})
  const [initial, setInitial] = useState<Record<string, Json>>({})
  const [meta, setMeta] = useState<FormRuntimeMeta>(createMeta)

  const [dirtyFields, setDirtyFields] = useState<Set<string>>(new Set())

  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})
  const [formError, setFormError] = useState<string | null>(null)

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [readonly, setReadonly] = useState(false)

  const valuesRef = useRef(values)
  const initialRef = useRef(initial)

  /* ================= SYNC REFS ================= */

  useEffect(() => {
    valuesRef.current = values
  }, [values])

  useEffect(() => {
    initialRef.current = initial
  }, [initial])

  const dirty = dirtyFields.size > 0

  /* ================= DIRTY ================= */

  const recalcDirty = useCallback(
    (nextValues: Record<string, Json>) => {
      const nextDirty = new Set<string>()

      for (const [key, value] of Object.entries(nextValues)) {
        if (value !== initialRef.current[key]) {
          nextDirty.add(key)
        }
      }

      setDirtyFields(nextDirty)
    },
    []
  )

  /* ================= INITIAL ================= */

  const setInitialValues = useCallback((init: Record<string, Json>) => {
    const normalized = Object.fromEntries(
      Object.entries(init).map(([key, value]) => [
        key,
        normalizeValue(value),
      ])
    )

    setValues(normalized)
    setInitial(normalized)
    setMeta(createMeta())

    setDirtyFields(new Set())
    setFieldErrors({})
    setFormError(null)
  }, [])

  /* ================= 🔥 setValue (FINAL) ================= */

  const setValue = useCallback((
    name: string,
    value: Json | ((prev: Json) => Json)
  ) => {
    let computedNext: Json

    setValues(prev => {
      const prevValue = prev[name]

      computedNext =
        typeof value === "function"
          ? (value as (v: Json) => Json)(prevValue)
          : value

      const next = {
        ...prev,
        [name]: computedNext,
      }

      valuesRef.current = next
      return next
    })

    setDirtyFields(prev => {
      const next = new Set(prev)

      const initialValue = initialRef.current[name]

      if (computedNext !== initialValue) {
        next.add(name)
      } else {
        next.delete(name)
      }

      return next
    })
  }, [])

  /* ================= PATCH ================= */

  const patch = useCallback((patchValues: Record<string, Json>) => {
    setValues(prev => {
      const next = {
        ...prev,
        ...patchValues,
      }

      valuesRef.current = next
      return next
    })

    recalcDirty({
      ...valuesRef.current,
      ...patchValues,
    })
  }, [recalcDirty])

  /* ================= RUNTIME ================= */

  const replaceRuntimeState = useCallback(
    (next: FormRuntimeState) => {
      setValues(next.values)
      valuesRef.current = next.values

      setMeta(next.meta)
      recalcDirty(next.values)
    },
    [recalcDirty]
  )

  /* ================= RESET ================= */

  const resetDirty = useCallback(() => {
    const nextInitial = { ...valuesRef.current }

    setInitial(nextInitial)
    initialRef.current = nextInitial

    setDirtyFields(new Set())
  }, [])

  /* ================= PAYLOAD ================= */

  const buildPayload = useCallback(
    (strategy: "all" | "dirty") => {
      const v = valuesRef.current

      if (strategy === "all") {
        return { ...v }
      }

      return Object.fromEntries(
        Array.from(dirtyFields).map(key => [key, v[key]])
      )
    },
    [dirtyFields]
  )

  /* ================= RETURN ================= */

  return useMemo(
    () => ({
      schema,
      values,
      meta,

      loading,
      saving,
      readonly,
      dirty,
      dirtyFields,

      fieldErrors,
      formError,

      setSchema,
      setInitialValues,
      setLoading,
      setSaving,
      setReadonly,
      setFieldErrors,
      setFormError,

      setValue,
      patch,
      replaceRuntimeState,
      resetDirty,
      buildPayload,
    }),
    [
      schema,
      values,
      meta,
      loading,
      saving,
      readonly,
      dirty,
      dirtyFields,
      fieldErrors,
      formError,
      setValue,
      patch,
      replaceRuntimeState,
      resetDirty,
      buildPayload,
    ]
  )
}