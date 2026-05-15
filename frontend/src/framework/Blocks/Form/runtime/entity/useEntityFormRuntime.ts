// ============================================================
// src/framework/Blocks/Form/runtime/entity/useEntityFormRuntime.ts
// ============================================================

import {
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react"

import isEqual from "fast-deep-equal"

import {
  useFormState,
} from "../base/useFormState"

import {
  useEntityLoader,
} from "./useEntityLoader"

import {
  useEntityOptionsLoader,
} from "./useEntityOptionsLoader"

import {
  useEntitySubmit,
} from "./useEntitySubmit"

import {
  usePageApi,
} from "@/framework/page/context/usePageApi"

import type {
  FormValues,
} from "../reactions/types"

import type {
  FormEntityConfig,
} from "../../types/FormConfig"

import type {
  ActionContext,
} from "@/framework/Blocks/Action/types"

import {
  useFormReactions,
} from "../reactions/useFormReactions"
import type { BlockCapabilities } from "@/framework/Blocks/BlockType"


export function useEntityFormRuntime(
  params: FormEntityConfig | null
) {

  /* =====================================================
     FORM STATE
  ===================================================== */

  const state =
    useFormState()

  /* =====================================================
     CAPABILITIES
  ===================================================== */

  const [
    capabilities,
    setCapabilities,
  ] = useState<BlockCapabilities>()

  /* =====================================================
     PAGE
  ===================================================== */

  const page = usePageApi()

  const {
    registerHandler,
    unregisterHandler,
    setDataKey,
  } = page

  /* =====================================================
     REFS
  ===================================================== */

  const prevValuesRef =
    useRef<FormValues | null>(null)

  const clearedRef =
    useRef<string | null>(null)

  const stateRef =
    useRef(state)

  useEffect(() => {
    stateRef.current = state
  }, [state])

  /* =====================================================
     RESOLVE RUNTIME
  ===================================================== */

  const resolvedObjectId =

    params?.objectId &&

    params.objectId !== "undefined" &&

    params.objectId !== "null"

      ? params.objectId

      : undefined

  const resolvedMode =

    params?.mode ??

    (
      resolvedObjectId
        ? "edit"
        : "create"
    )

  /* =====================================================
     LOAD
  ===================================================== */

  useEntityLoader({

    entity:
      params?.entity,

    mode:
      resolvedMode,

    objectId:
      resolvedObjectId,

    state,

    onCapabilities:
      setCapabilities,
  })

  /* =====================================================
     OPTIONS
  ===================================================== */

  useEntityOptionsLoader(state)

  /* =====================================================
     REACTIONS
  ===================================================== */

  useFormReactions({
    state,
  })

  /* =====================================================
     ACTION: setValue
  ===================================================== */

  const setValueHandler =
    useMemo(() => ({

      id: "form:setValue",

      run: (
        ctx: ActionContext
      ) => {

        const payload =
          ctx.payload as {

            field: string

            value: string

            mode?:
              | "append"
              | "replace"

          } | undefined

        if (!payload) {
          return
        }

        const current =

          stateRef.current
            .values[payload.field]

        const nextValue =

          payload.mode === "append"

            ? `${typeof current === "string" ? current : ""}${payload.value}`

            : payload.value

        stateRef.current.setValue(
          payload.field,
          nextValue
        )
      },
    }), [])

  useEffect(() => {

    registerHandler(
      "form:setValue",
      setValueHandler
    )

    return () => {

      unregisterHandler(
        "form:setValue",
        setValueHandler.id
      )
    }

  }, [

    registerHandler,

    unregisterHandler,

    setValueHandler,
  ])

  /* =====================================================
     SYNC DATA (edit)
  ===================================================== */

  useEffect(() => {

    if (!params?.entity) {
      return
    }

    if (
      resolvedMode !== "edit"
    ) {
      return
    }

    const values =
      state.values as FormValues

    if (!values) {
      return
    }

    if (
      Object.keys(values)
        .length === 0
    ) {
      return
    }

    if (
      isEqual(
        prevValuesRef.current,
        values
      )
    ) {
      return
    }

    prevValuesRef.current =
      values

    setDataKey(
      params.entity,
      values
    )

  }, [

    params?.entity,

    resolvedMode,

    state.values,

    setDataKey,
  ])

  /* =====================================================
     CLEAR DATA (create)
  ===================================================== */

  useEffect(() => {

    if (!params?.entity) {
      return
    }

    if (
      resolvedMode === "create"
    ) {

      if (
        clearedRef.current ===
        params.entity
      ) {
        return
      }

      clearedRef.current =
        params.entity

      prevValuesRef.current =
        null

      setDataKey(
        params.entity,
        undefined
      )
    }

  }, [

    params?.entity,

    resolvedMode,

    setDataKey,
  ])

  /* =====================================================
     SUBMIT
  ===================================================== */

  const submit =
    useEntitySubmit({

      entity:
        params?.entity,

      mode:
        resolvedMode,

      objectId:
        resolvedObjectId,

      state,

      redirect:
        params?.submit?.redirect,
    })

  /* =====================================================
     VALIDATE
  ===================================================== */

  const validate = () => {

    if (!params) {
      return false
    }

    if (
      resolvedMode === "view"
    ) {
      return false
    }

    return true
  }

  /* =====================================================
     RETURN
  ===================================================== */

  return {

    ...state,

    capabilities,

    submit,

    validate,
  }
}