import { useEffect } from "react"

import {
  loadFormSchema,
} from "@/framework/api/form/loadFormSchema"

import {
  parseApiError,
} from "@/framework/utils/parseApiError"

import {
  traceRuntime,
} from "@/framework/trace/runtime"

import {
  adaptFormSchema,
} from "../../config/adaptFormSchema"

import type {
  FormState,
} from "../base/useFormState"

import type {
  EntityFormMode,
} from "../../types/runtime"

import type {
  Json,
} from "@/framework/types/json"

import {

  resolveWithContext,

  toPlainSnapshot,

} from "@/framework/bind/runtime/bindRuntime"

import {
  usePageRuntimeContext,
} from "@/framework/page/runtime/usePageRuntimeContext"
import type { BlockCapabilities } from "@/framework/Blocks/BlockType"


/* =========================================================
   PARAMS
   ========================================================= */

type Params = {

  entity?: string

  mode?: EntityFormMode

  objectId?: string | number | null

  initial?: Record<string, Json>

  state: FormState

  // 🔥 NEW
  onCapabilities?: (
    capabilities?: BlockCapabilities
  ) => void
}

/* =========================================================
   LOADER
   ========================================================= */

export function useEntityLoader({

  entity,

  mode,

  objectId,

  initial,

  state,

  onCapabilities,

}: Params) {

  const runtime =
    usePageRuntimeContext()

  const query =
    runtime?.query ?? {}

  const queryKey =
    JSON.stringify(query)

  const initialKey =
    JSON.stringify(initial ?? {})

  useEffect(() => {

    if (!entity) {

      state.setLoading(false)

      return
    }

    let cancelled = false

    const apiMode:
      "create" | "edit" =

      objectId !== undefined &&
      objectId !== null

        ? "edit"

        : "create"

    const safeObjectId =

      objectId === null ||
      objectId === undefined

        ? undefined

        : objectId

    /* =====================================================
       EXEC
       ===================================================== */

    const exec = async () => {

      state.setLoading(true)

      state.setFormError(null)

      state.setFieldErrors({})

      const resolvedInitial = initial

        ? resolveWithContext(
            toPlainSnapshot(initial),
            runtime
          )

        : undefined

      console.log(
        "🔥 FORM QUERY:",
        query
      )

      console.log(
        "🔥 RESOLVED INITIAL:",
        resolvedInitial
      )

      /* ===================================================
         API
         =================================================== */

      const api =
        await loadFormSchema(

          entity,

          apiMode,

          safeObjectId,

          query
        )

      if (cancelled) {
        return
      }

      /* ===================================================
         CAPABILITIES
         =================================================== */

      onCapabilities?.(
        api.capabilities
      )

      console.log(
        "🛡 FORM CAPABILITIES:",
        api.capabilities
      )

      /* ===================================================
         SCHEMA
         =================================================== */

      const ui =
        adaptFormSchema(api)

      state.setSchema(ui)

      /* ===================================================
         INITIAL VALUES
         =================================================== */

      const finalInitial = {

        ...(resolvedInitial ?? {}),

        ...(ui.initial ?? {}),
      }

      if (
        Object.keys(finalInitial)
          .length > 0
      ) {

        console.log(
          "🟢 FINAL INITIAL:",
          finalInitial
        )

        state.setInitialValues(
          finalInitial
        )
      }
    }

    /* =====================================================
       RUN
       ===================================================== */

    const run = async () => {

      const trace =
        traceRuntime.current()

      try {

        if (trace) {

          await trace.step(

            "entity_form_load",

            exec,

            {
              entity,

              mode,

              objectId:
                safeObjectId,

              queryKeys:
                Object.keys(query),

              initialKeys:
                initial
                  ? Object.keys(initial)
                  : [],
            }
          )

        } else {

          await exec()
        }

      } catch (e) {

        const err =
          parseApiError(e)

        if (!cancelled) {

          state.setFormError(
            err.message
          )
        }

      } finally {

        if (!cancelled) {

          state.setLoading(false)
        }
      }
    }

    run()

    return () => {
      cancelled = true
    }

  }, [

    entity,

    mode,

    objectId,

    queryKey,

    initialKey,
  ])
}