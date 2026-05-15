// ============================================================
// src/framework/Blocks/Form/runtime/base/useFormState.ts
// ============================================================

import {
  useCallback,
  useMemo,
  useState,
} from "react"

import type { Json }
  from "@/framework/types/json"

import type { FormSchema }
  from "../../types/types"

import type {
  BlockCapabilities,
} from "@/framework/Blocks/BlockType"

/* ============================================================
   TYPES
   ============================================================ */

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

  // 🔥 NEW
  capabilities?: BlockCapabilities

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

  // 🔥 NEW
  setCapabilities: (
    capabilities?: BlockCapabilities
  ) => void

  resetDirty: () => void

  reset: () => void

  buildPayload: (
    mode?: "all" | "dirty"
  ) => FormValues
}

/* ============================================================
   PARAMS
   ============================================================ */

type Params = {
  initial?: FormValues
  readonly?: boolean
}

/* ============================================================
   STATE
   ============================================================ */

export function useFormState({
  initial = {},
  readonly = false,
}: Params = {}): FormState {

  /* ========================================================
     VALUES
     ======================================================== */

  const [
    values,
    setValuesState,
  ] = useState<FormValues>(initial)

  const [
    initialValues,
    setInitialValuesState,
  ] = useState<FormValues>(initial)

  /* ========================================================
     ERRORS
     ======================================================== */

  const [
    fieldErrors,
    setFieldErrorsState,
  ] = useState<FieldErrors>({})

  const [
    formError,
    setFormError,
  ] = useState<string | null>(null)

  /* ========================================================
     SCHEMA
     ======================================================== */

  const [
    schema,
    setSchemaState,
  ] = useState<FormSchema | null>(null)

  /* ========================================================
     CAPABILITIES
     ======================================================== */

  const [
    capabilities,
    setCapabilitiesState,
  ] = useState<BlockCapabilities>()

  /* ========================================================
     FLAGS
     ======================================================== */

  const [
    dirty,
    setDirty,
  ] = useState(false)

  const [
    loading,
    setLoading,
  ] = useState(false)

  const [
    saving,
    setSaving,
  ] = useState(false)

  /* ========================================================
     SET VALUE
     ======================================================== */

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

        const next = {
          ...prev,
        }

        delete next[name]

        return next
      })
    },

    []
  )

  /* ========================================================
     SET VALUES
     ======================================================== */

  const setValues = useCallback(

    (
      next: FormValues
    ) => {

      setValuesState(next)

      setDirty(true)
    },

    []
  )

  /* ========================================================
     INITIAL VALUES
     ======================================================== */

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

  /* ========================================================
     FIELD ERRORS
     ======================================================== */

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

  /* ========================================================
     CLEAR FIELD ERROR
     ======================================================== */

  const clearFieldError =
    useCallback(

      (
        name: string
      ) => {

        setFieldErrorsState(prev => {

          if (!prev[name]) {
            return prev
          }

          const next = {
            ...prev,
          }

          delete next[name]

          return next
        })
      },

      []
    )

  /* ========================================================
     SCHEMA
     ======================================================== */

  const setSchema = useCallback(

    (
      next: FormSchema | null
    ) => {

      setSchemaState(next)
    },

    []
  )

  /* ========================================================
     CAPABILITIES
     ======================================================== */

  const setCapabilities =
    useCallback(

      (
        next?: BlockCapabilities
      ) => {

        setCapabilitiesState(next)
      },

      []
    )

  /* ========================================================
     RESET DIRTY
     ======================================================== */

  const resetDirty =
    useCallback(() => {

      setDirty(false)

    }, [])

  /* ========================================================
     RESET
     ======================================================== */

  const reset =
    useCallback(() => {

      setValuesState(initialValues)

      setFieldErrorsState({})

      setFormError(null)

      setDirty(false)

      setSaving(false)

    }, [initialValues])

  /* ========================================================
     BUILD PAYLOAD
     ======================================================== */

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

  /* ========================================================
     RETURN
     ======================================================== */

  return useMemo(() => ({

    values,

    initialValues,

    fieldErrors,

    formError,

    schema,

    // 🔥 NEW
    capabilities,

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

    // 🔥 NEW
    setCapabilities,

    resetDirty,

    reset,

    buildPayload,

  }), [

    values,

    initialValues,

    fieldErrors,

    formError,

    schema,

    // 🔥 NEW
    capabilities,

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

    // 🔥 NEW
    setCapabilities,

    resetDirty,

    reset,

    buildPayload,
  ])
}