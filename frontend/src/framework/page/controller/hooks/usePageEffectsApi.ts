import type { ActionContext } from "@/framework/Blocks/Action/types"
import { useToast } from "@/framework/page/runtime/effects/handlers/toast/useToast"
import { usePageEffectsRuntime } from "@/framework/page/runtime/effects/usePageEffectsRuntime"

type Params = {
  navigate: (
    page: string,
    ctx?: ActionContext
  ) => void

  setDataKey: (
    key: string,
    value: unknown
  ) => void

  emit: (
    event: string,
    payload?: unknown
  ) => void
}

export function usePageEffectsApi({
  navigate,
  setDataKey,
  emit,
}: Params) {
  const toast = useToast()

  console.log(
    "[PageEffectsApi] toast instance",
    toast
  )

  return usePageEffectsRuntime({
    navigate,
    setDataKey,
    emit,
    toast: (message, variant) => {
      console.log("[PageEffectsApi] toast", {
        message,
        variant,
      })

      console.log(
        "[PageEffectsApi] toast.show exists",
        !!toast.show
      )

      toast.show({
        title: message,
        variant: variant ?? "info",
      })
    },
  })
}