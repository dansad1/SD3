import { usePageController } from "../controller/PageController"
import type { ApiPageSchema } from "../PageSchema"
import { useBind } from "./bind"
import { useNormalize } from "./normalize"
import { usePhysical } from "./physical"

export function usePageRuntime(schema: ApiPageSchema) {
  const ctrl = usePageController()

  const pageId = schema.id || schema.title || "page"

  // ❗ БЕРЁМ ОТСЮДА
  const ctx = ctrl.runtimeContext

  const semantic = useNormalize(schema, pageId)

  const bound = useBind(semantic, ctx, pageId)

  const physicalTree = usePhysical(bound, pageId)

  return {
    ctrl,
    physicalTree,
  }
}