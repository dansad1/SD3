import { useCallback } from "react"
import { traceRuntime } from "@/framework/trace/runtime"
import { usePageApi } from "@/framework/page/context/usePageApi"
import type { PageEffect } from "@/framework/page/runtime/effects/types"
import { api } from "@/framework/api/client"

type DeleteResult = {
  status?: "ok" | "error"
  message?: string
  effects?: PageEffect[]
}

export function useTableDelete(
  entity: string,
  enabled: boolean = true
) {
  const page = usePageApi()

  return useCallback(
    async (id: string | number) => {
      if (!enabled) {
        return false
      }

      const exec = () =>
        api.delete<DeleteResult>(
          `/entity/${entity}/${id}/`
        )

      const trace = traceRuntime.current()

      try {
        const result = !trace
          ? await exec()
          : await trace.step(
              "table_row_delete",
              exec,
              {
                block: "Table",
                entity,
                objectId: id,
              }
            )

        if (result?.effects) {
          page.runEffects(result.effects)
        }

        if (result?.message) {
          page.runEffect({
            type: "toast",
            variant: "success",
            message: result.message,
          })
        }

        return true
      } catch (error) {
        console.error(
          "❌ TABLE DELETE ERROR",
          error
        )

        page.runEffect({
          type: "toast",
          variant: "error",
          message: "Не удалось удалить запись",
        })

        return false
      }
    },
    [entity, enabled, page]
  )
}