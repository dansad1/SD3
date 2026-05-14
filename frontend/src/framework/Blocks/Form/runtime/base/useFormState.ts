// src/framework/Blocks/Form/runtime/base/useFormState.ts

import {
  useCallback,
  useMemo,
  useState,
} from "react"

import type { Json }
  from "@/framework/types/json"

import type { FormSchema }
  from "../../types/types"

export type FormValues =
  Record<string, Json>

export type FieldErrors =
  Record<string, string[]>

export type FormState = {
  values: FormValues
  initialValues: FormValues

  fieldErrors: FieldErrors
  formError: string | null

  schema: FormSchema | null

  dirty: boolean
  loading: boolean
  saving: boolean
  readonly: boolean

  setValue: (
    name: string,
    value: Json
  ) => void

  setValues: (
    values: FormValues
  ) => void

  setInitialValues: (
    values: FormValues
  ) => void

  setFieldErrors: (
    errors: FieldErrors
  ) => void

  clearFieldError: (
    name: string
  ) => void

  setFormError: (
    value: string | null
  ) => void

  setLoading: (
    value: boolean
  ) => void

  setSaving: (
    value: boolean
  ) => void

  setDirty: (
    value: boolean
  ) => void

  setSchema: (
    schema: FormSchema | null
  ) => void

  resetDirty: () => void

  reset: () => void

  buildPayload: (
    mode?: "all" | "dirty"
  ) => FormValues
}

type Params = {
  initial?: FormValues
  readonly?: boolean
}

export function useFormState({
  initial = {},
  readonly = false,
}: Params = {}): FormState {
  const [values, setValuesState] =
    useState<FormValues>(initial)

  const [
    initialValues,
    setInitialValuesState,
  ] = useState<FormValues>(initial)

  const [
    fieldErrors,
    setFieldErrorsState,
  ] = useState<FieldErrors>({})

  const [
    formError,
    setFormError,
  ] = useState<string | null>(null)

  const [
    schema,
    setSchemaState,
  ] = useState<FormSchema | null>(null)

  const [dirty, setDirty] =
    useState(false)

  const [loading, setLoading] =
    useState(false)

  const [saving, setSaving] =
    useState(false)

  const setValue = useCallback(
    (
      name: string,
      value: Json
    ) => {
      setValuesState(prev => ({
        ...prev,
        [name]: value,
      }))

      setDirty(true)

      setFieldErrorsState(prev => {
        if (!prev[name]) {
          return prev
        }

        const next = { ...prev }
        delete next[name]

        return next
      })
    },
    []
  )

  const setValues = useCallback(
    (
      next: FormValues
    ) => {
      setValuesState(next)
      setDirty(true)
    },
    []
  )

  const setInitialValues =
    useCallback(
      (
        next: FormValues
      ) => {
        setInitialValuesState(next)
        setValuesState(next)
        setDirty(false)
      },
      []
    )

  const setFieldErrors =
    useCallback(
      (
        errors: FieldErrors
      ) => {
        console.log(
          "🧨 SET FIELD ERRORS",
          errors
        )

        setFieldErrorsState(errors)
      },
      []
    )

  const clearFieldError =
    useCallback(
      (
        name: string
      ) => {
        setFieldErrorsState(prev => {
          if (!prev[name]) {
            return prev
          }

          const next = { ...prev }
          delete next[name]

          return next
        })
      },
      []
    )

  const setSchema = useCallback(
    (
      next: FormSchema | null
    ) => {
      setSchemaState(next)
    },
    []
  )

  const resetDirty =
    useCallback(() => {
      setDirty(false)
    }, [])

  const reset =
    useCallback(() => {
      setValuesState(initialValues)
      setFieldErrorsState({})
      setFormError(null)
      setDirty(false)
      setSaving(false)
    }, [initialValues])

  const buildPayload =
    useCallback(
      (
        _mode:
          | "all"
          | "dirty" = "all"
      ) => {
        return values
      },
      [values]
    )

  return useMemo(() => ({
    values,
    initialValues,

    fieldErrors,
    formError,

    schema,

    dirty,
    loading,
    saving,
    readonly,

    setValue,
    setValues,
    setInitialValues,

    setFieldErrors,
    clearFieldError,
    setFormError,

    setLoading,
    setSaving,
    setDirty,

    setSchema,

    resetDirty,
    reset,

    buildPayload,
  }), [
    values,
    initialValues,
    fieldErrors,
    formError,
    schema,
    dirty,
    loading,
    saving,
    readonly,
    setValue,
    setValues,
    setInitialValues,
    setFieldErrors,
    clearFieldError,
    setSchema,
    resetDirty,
    reset,
    buildPayload,
  ])
}