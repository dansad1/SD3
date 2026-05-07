import { useEffect } from "react"
import { traceRuntime } from "@/framework/trace/runtime"

import { useFormState } from "../base/useFormState"
import type { FormBlock, FormSchema } from "../../types/types"
import { api } from "@/framework/api/client"

type FormState = ReturnType<typeof useFormState<FormSchema>>

type Option = {
  value: string | number
  label: string
}

export function useEntityOptionsLoader(state: FormState) {

  const schema = state.schema

  useEffect(() => {

    if (!schema) return

    const blocks = schema.blocks

    const fieldBlocks = blocks.filter(
      (b: FormBlock): b is Extract<FormBlock, { type: "field" }> =>
        b.type === "field"
    )

    const targets = fieldBlocks.filter(
      (b) => b.field.entity && !b.field.choices
    )

    if (targets.length === 0) return

    let cancelled = false

    const load = async () => {

      const trace = traceRuntime.current()

      const exec = async () => {

        const results = await Promise.all(
          targets.map((b) =>
            api.get<{ items: Option[] }>(
              `/entity/${b.field.entity}/options`
            )
          )
        )

        if (cancelled) return

        const map = new Map<string, { items: Option[] }>(
          targets.map((b, i) => [b.field.name, results[i]])
        )

        const updatedBlocks = blocks.map((b: FormBlock) => {

          if (b.type !== "field") return b

          const res = map.get(b.field.name)
          if (!res) return b

          return {
            ...b,
            field: {
              ...b.field,
              choices: res.items ?? [],
            },
          }
        })

        state.setSchema({
          ...schema,
          blocks: updatedBlocks,
        })

      }

      if (!trace) {
        try {
          await exec()
        } catch (e) {
          console.error("options load failed", e)
        }
        return
      }

      await trace.step("entity_options_load", exec)

    }

    load()

    return () => {
      cancelled = true
    }

  }, [schema]) // eslint-disable-line react-hooks/exhaustive-deps
}