import type { ActionContext } from "@/framework/Blocks/Action/types"
import { usePageApi } from "@/framework/page/context/usePageApi"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import { resolveAction } from "../resolveAction"
import { executeResolvedAction } from "./executeResolvedAction"
import { mergeActionContext } from "./mergeActionContext"
import { handleActionResult } from "./handleActionResult"


// useActionExecutor.ts

export function useActionExecutor() {
  const page = usePageApi()
  const runtimeContext = usePageRuntimeContext()

  const runAction = async (
    target: string,
    ctx: ActionContext = {}
  ): Promise<unknown> => {
    console.log("🚀 RUN ACTION START", {
      target,
      ctx,
      runtimeContext,
    })

    if (!target) {
      console.warn("⚠️ runAction: empty target")
      return false
    }

    const started = page.loading.start(target)

    if (!started) {
      console.warn("⚠️ ACTION ALREADY RUNNING", {
        target,
      })

      return false
    }

    try {
      const mergedCtx = mergeActionContext(
        runtimeContext,
        ctx
      )

      console.log("🧩 RUN ACTION MERGED CTX", {
        target,
        runtimeContext,
        ctx,
        mergedCtx,
      })

      const resolved = resolveAction(target)

      console.log("🧩 RUN ACTION RESOLVED", {
        target,
        resolved,
      })

      const result = await executeResolvedAction({
        page,
        resolved,
        mergedCtx,
      })

      console.log("🧩 RUN ACTION RESULT", {
        target,
        result,
      })

      handleActionResult(page, result)

      return result
    } catch (error) {
      console.error("❌ ACTION EXECUTION FAILED", {
        target,
        ctx,
        error,
      })

      page.runEffect({
        type: "toast",
        variant: "error",
        message: "Не удалось выполнить действие",
      })

      return false
    } finally {
      page.loading.finish(target)
    }
  }

  return {
    runAction,
    isRunning: page.loading.isRunning,
  }
}