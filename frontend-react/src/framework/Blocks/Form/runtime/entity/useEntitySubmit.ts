// useEntitySubmit.ts

import { useCallback } from "react"
import { traceRuntime } from "@/framework/trace/runtime"
import { usePageApi } from "@/framework/page/context/usePageApi"

import type { EntityFormMode } from "../../types/runtime"
import type { FormState } from "../base/useFormState"

import { resolveApiMode } from "./submit/resolveApiMode"
import { executeEntitySubmit } from "./submit/executeEntitySubmit"
import { handleSubmitError } from "./submit/handleSubmitError"

type RedirectTarget =
  | string
  | {
      to: string
      ctx?: Record<string, unknown>
    }

type Params = {
  entity?: string
  mode?: EntityFormMode
  objectId?: string | number
  state: FormState
  redirect?: RedirectTarget
}

export function useEntitySubmit({
  entity,
  mode,
  objectId,
  state,
  redirect,
}: Params) {
  const page = usePageApi()

  return useCallback(async () => {
    console.log("🧪 SUBMIT ENTRY", {
      entity,
      mode,
      objectId,
      dirty: state.dirty,
      readonly: state.readonly,
      saving: state.saving,
      values: state.values,
    })

    if (!entity || state.saving || state.readonly) {
      console.warn("❌ SUBMIT BLOCKED", {
        entity,
        saving: state.saving,
        readonly: state.readonly,
      })

      return false
    }

    const trace = traceRuntime.current()
    const apiMode = resolveApiMode(mode)

    const exec = async () => {
      try {
        return await executeEntitySubmit({
          page,
          entity,
          apiMode,
          objectId,
          state,
          redirect,
        })
      } catch (error) {
        handleSubmitError(
          error,
          state,
          page
        )

        return false
      }
    }

    if (!trace) {
      return await exec()
    }

    try {
      const result = await trace.step(
        "entity_form_submit",
        exec
      )

      return result === false ? false : true
    } catch (error) {
      console.error("❌ TRACE SUBMIT ERROR", error)

      page.runEffect({
        type: "toast",
        variant: "error",
        message: "Не удалось сохранить форму",
      })

      return false
    }
  }, [
    entity,
    mode,
    objectId,
    state,
    redirect,
    page,
  ])
}