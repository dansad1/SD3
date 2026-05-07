// form/hooks/submit/executeEntitySubmit.ts

import { saveFormData } from "@/framework/api/form/saveFormData"
import type { PageApi } from "@/framework/page/context/types"
import { buildSubmitPayload } from "./buildSubmitPayload"
import { resolveRedirectTarget } from "./resolveRedirectTarget"
import { handleSubmitError } from "./handleSubmitError"

import type { FormState } from "../../base/useFormState"

type RedirectTarget =
  | string
  | {
      to: string
      ctx?: Record<string, unknown>
    }

type Params = {
  page: PageApi
  entity: string
  apiMode: "create" | "edit"
  objectId?: string | number
  state: FormState
  redirect?: RedirectTarget
}

export async function executeEntitySubmit({
  page,
  entity,
  apiMode,
  objectId,
  state,
  redirect,
}: Params): Promise<boolean> {
  const payload = buildSubmitPayload(
    apiMode,
    state
  )

  console.log("💾 SUBMIT PAYLOAD MODE", {
    dirty: state.dirty,
    payloadMode:
      apiMode === "create"
        ? "all"
        : state.dirty
          ? "dirty"
          : "all",
    payload,
  })

  state.setSaving(true)
  state.setFormError(null)
  state.setFieldErrors({})

  try {
    const result = await saveFormData(
      entity,
      payload,
      apiMode,
      objectId
    )

    console.log("✅ SUBMIT RESULT", result)
    console.log(
      "🧪 SUBMIT EFFECTS",
      result.effects
    )

    if (result.effects?.length) {
      await page.runEffects(result.effects)
    } else {
      await page.runEffects([
        {
          type: "toast",
          variant: "success",
          message:
            apiMode === "create"
              ? "Запись успешно создана"
              : "Изменения успешно сохранены",
        },
      ])
    }

    state.resetDirty()

    const target = resolveRedirectTarget(
      redirect,
      result.redirect
    )

    if (target) {
      if (typeof target === "string") {
        page.navigate(target)
      } else {
        page.navigate(
          target.to,
          target.ctx
        )
      }
    }

    return true
  } catch (error) {
    console.error(
      "❌ ENTITY SUBMIT FAILED",
      error
    )

    await handleSubmitError(
      error,
      state,
      page
    )

    return false
  } finally {
    state.setSaving(false)
  }
}