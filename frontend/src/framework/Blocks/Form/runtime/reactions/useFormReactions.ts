import { useEffect, useMemo, useRef } from "react"
import isEqual from "fast-deep-equal"

import { usePageApi } from "@/framework/page/context/usePageApi"

import type { FormSchema } from "../../types/types"
import type { FormRuntimeState, Reaction } from "./types"
import type { FormState } from "../base/useFormState"

import { shallowChangedFields } from "./utils"
import { runReactions } from "./runReactions"

import type { PageEffect } from "@/framework/page/runtime/effects/types"

type UseFormReactionsParams = {
  state: FormState
}

export function useFormReactions({
  state,
}: UseFormReactionsParams) {
  const page = usePageApi()

  const { values, meta, replaceRuntimeState, schema } = state

  const prevValuesRef = useRef(values)
  const runIdRef = useRef(0)

  const typedSchema = schema as FormSchema | null

  const reactions: Reaction[] = useMemo(
    () => typedSchema?.reactions ?? [],
    [typedSchema]
  )

  useEffect(() => {
    if (!typedSchema) return

    if (reactions.length === 0) {
      prevValuesRef.current = values
      return
    }

    const prev = prevValuesRef.current
    const next = values

    const changedFields = shallowChangedFields(prev, next)

    if (changedFields.length === 0) return

    prevValuesRef.current = next

    const runId = ++runIdRef.current

    const currentRuntimeState: FormRuntimeState = {
      values: next,
      meta,
    }

    const exec = async () => {
      const result = await runReactions({
        state: currentRuntimeState,
        reactions,
        changedFields,
        runPageEffect: (effect: PageEffect) => {
          page.runEffect(effect)
        },
      })

      if (runId !== runIdRef.current) return

      if (
        isEqual(result.values, values) &&
        isEqual(result.meta, meta)
      ) {
        return
      }

      replaceRuntimeState(result)
      prevValuesRef.current = result.values
    }

    exec().catch(error => {
      console.error("[form reactions] failed", error)
    })

  }, [
    typedSchema,
    reactions,
    values,
    meta,
    replaceRuntimeState,
    page,
  ])
}