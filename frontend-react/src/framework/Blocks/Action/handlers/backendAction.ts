import type { PageApi } from "@/framework/page/context/types"
import { buildBackendContext } from "../buildBackendContext"
import type { ActionContext } from "../types"
import { submitAction } from "@/framework/api/action/submitAction"

export async function runBackendAction(
  page: PageApi,
  code: string,
  ctx: ActionContext
): Promise<boolean> {
  const backendCtx = buildBackendContext(ctx)

  console.log("🌐 BACKEND ACTION REQUEST", {
    code,
    backendCtx,
  })

  const result = await submitAction(
    code,
    {},
    backendCtx
  )

  console.log("🌐 BACKEND ACTION RAW RESULT", {
    code,
    result,
    status: result?.status,
    message: result?.message,
  })

  if (!result) {
    console.warn("❌ BACKEND ACTION EMPTY RESULT", code)
    return false
  }

  if (result.status === "error") {
    console.error("❌ BACKEND ACTION ERROR RESULT", {
      code,
      result,
    })

    return false
  }

  if (result?.redirect) {
    page.navigate(String(result.redirect), ctx)
  }

  return true
}