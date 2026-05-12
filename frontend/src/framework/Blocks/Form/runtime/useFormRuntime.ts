import { useMemo } from "react"

import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import { bindFormConfig } from "@/framework/Blocks/Form/config/bindFormConfig"

import { useEntityFormRuntime } from "./entity/useEntityFormRuntime"
import { useActionFormRuntime } from "./action/useActionFormRuntime"

import type { FormConfig } from "../types/FormConfig"
import type { Json } from "@/framework/types/json"

export function useFormRuntime(config: FormConfig) {
  const runtime = usePageRuntimeContext()

  // 🔥 DSL → runtime
  const boundConfig = useMemo(() => {
    return bindFormConfig(config, {
      query: runtime.query,
      params: runtime.params,
      data: runtime.data as Record<string, Json>,
    })
  }, [
    config,
    runtime.params,
    runtime.query,
    runtime.data,
  ])

  const entityRuntime = useEntityFormRuntime(
    boundConfig.formType === "entity" ? boundConfig : null
  )

  const actionRuntime = useActionFormRuntime(
    boundConfig.formType === "action" ? boundConfig : null
  )

  return boundConfig.formType === "entity"
    ? entityRuntime
    : actionRuntime
}