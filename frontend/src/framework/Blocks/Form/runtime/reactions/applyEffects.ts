import { api } from "@/framework/api/client"

import type {
  FormEffect,
  FormRuntimeState,
  RunPageEffect,
} from "./types"

import { getByPath } from "./utils"

export function applyLocalEffects(
  state: FormRuntimeState,
  effects: FormEffect[],
  runPageEffect?: RunPageEffect
): FormRuntimeState {
  const next: FormRuntimeState = {
    values: { ...state.values },
    meta: {
      visible: { ...state.meta.visible },
      disabled: { ...state.meta.disabled },
    },
  }

  for (const effect of effects) {
    switch (effect.type) {
      case "set":
        next.values[effect.field] = effect.value
        break

      case "clear":
        next.values[effect.field] = null
        break

      case "patch":
        next.values = {
          ...next.values,
          ...effect.values,
        }
        break

      case "visible":
        next.meta.visible[effect.field] = effect.value
        break

      case "disabled":
        next.meta.disabled[effect.field] = effect.value
        break

      case "page":
        runPageEffect?.(effect.effect)
        break

      case "fetch":
        break
    }
  }

  return next
}

export async function applyAsyncEffects(
  state: FormRuntimeState,
  effects: FormEffect[]
): Promise<FormRuntimeState> {
  let next = state

  for (const effect of effects) {
    if (effect.type !== "fetch") continue

    const res = await api.get<unknown>(effect.url)

    const patch: FormRuntimeState["values"] = {}

    for (const [field, path] of Object.entries(effect.map)) {
      const value = getByPath<FormRuntimeState["values"][string]>(
        res,
        path
      )

      if (value !== undefined) {
        patch[field] = value
      }
    }

    if (Object.keys(patch).length > 0) {
      next = {
        ...next,
        values: {
          ...next.values,
          ...patch,
        },
      }
    }
  }

  return next
}