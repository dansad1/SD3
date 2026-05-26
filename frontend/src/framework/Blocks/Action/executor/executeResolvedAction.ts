import type { Json } from "@/framework/types/json"
import { submitAction } from "@/framework/api/action/submitAction"
import type { PageApi } from "@/framework/page/context/types"
import type { ResolvedAction } from "../resolveAction"
import type { ActionContext } from "@/framework/Blocks/Action/types"
import { actionRegistry } from "../registry"

type Params = {
  page: PageApi
  resolved: ResolvedAction
  mergedCtx: ActionContext
}

export async function executeResolvedAction({
  page,
  resolved,
  mergedCtx,
}: Params) {
  console.log("⚙️ executeResolvedAction:start", {
    resolved,
    mergedCtx,
  })

  /* =========================
     NAVIGATE
  ========================= */

  if (resolved.kind === "navigate") {
    console.log("➡️ navigate", resolved.to)

    return page.navigate(
      resolved.to,
      mergedCtx
    )
  }

  /* =========================
     BACKEND ACTION
  ========================= */

  if (resolved.kind === "backend") {
    console.log("🛰 backend action", resolved.code)

    const result = await submitAction(
      resolved.code,
      {},
      mergedCtx as Record<string, Json>
    )

    console.log("🛰 backend result", result)

    /* DOWNLOAD */

    if (
      result &&
      typeof result === "object" &&
      "download" in result &&
      typeof result.download === "string"
    ) {
      const link = document.createElement("a")
      link.href = result.download
      link.target = "_blank"
      link.rel = "noopener"

      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }

    /* REDIRECT */

    if (
      result &&
      typeof result === "object" &&
      "redirect" in result &&
      typeof result.redirect === "string"
    ) {
      page.navigate(result.redirect)
    }

    return result
  }

  /* =========================
     UI ACTION (🔥 ФИКС ЗДЕСЬ)
  ========================= */

  if (resolved.kind === "ui") {
    console.log("🧩 ui action", resolved.id)

    const action = actionRegistry.get(resolved.id)

    if (!action) {
      console.warn("❌ UI ACTION NOT FOUND", resolved.id)
      return null
    }

    return await action.run(mergedCtx)
  }

  /* =========================
     PAGE ACTION (оставляем)
  ========================= */

  if (resolved.kind === "page") {
    console.log("📄 page action", resolved.id)

    return page.run(
      resolved.id,
      mergedCtx
    )
  }

  /* =========================
     FALLBACK
  ========================= */

  console.warn("⚠️ unknown action kind", resolved)

  return null
}