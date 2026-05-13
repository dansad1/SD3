import { PhysicalRenderer } from "@/framework/physical/build/PhysicalRenderer"

import type { ActionDescriptor } from "@/framework/Blocks/Action/types"
import type { PhysicalNode } from "@/framework/physical/types/PhysicalNode"
import type { ApiPageSchema } from "../PageSchema"
import { PageFooter } from "./PageFooter"
import { useActionExecutor } from "@/framework/Blocks/Action/executor/useActionExecutor"

export function PageView({
  schema,
  physicalTree,
  actions,

}: {
  schema: ApiPageSchema
  physicalTree: PhysicalNode | null
  actions: ActionDescriptor[]
}) {

  const executor = useActionExecutor()

  const runAction =
    executor?.runAction ??
    (async () => false)

  const pageReady =
    physicalTree?.kind === "layout" &&
    physicalTree.children.length > 0

  return (
    <div className="page-container">

      {schema.title && <h1>{schema.title}</h1>}

      {physicalTree && (
        <PhysicalRenderer node={physicalTree} />
      )}

      {pageReady && actions.length > 0 && (
        <PageFooter
          actions={actions}
          run={runAction}
        />
      )}

    </div>
  )
}