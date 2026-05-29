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



  return usePageEffectsRuntime({
    navigate,
    setDataKey,
    emit,
    toast: (message, variant) => {
    

      toast.show({
        title: message,
        variant: variant ?? "info",
      })
    },
  })
}