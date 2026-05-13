// src/framework/page/render/PageView.tsx

import { PhysicalRenderer }
  from "@/framework/physical/build/PhysicalRenderer"

import type { ActionDescriptor }
  from "@/framework/Blocks/Action/types"

import type { PhysicalNode }
  from "@/framework/physical/types/PhysicalNode"

import type { ApiPageSchema }
  from "../PageSchema"

import { PageFooter }
  from "./PageFooter"

import { useActionExecutor }
  from "@/framework/Blocks/Action/executor/useActionExecutor"


export function PageView({

  schema,

  physicalTree,

  actions,

}: {

  schema: ApiPageSchema

  physicalTree: PhysicalNode | null

  actions: ActionDescriptor[]
}) {

  // =====================================================
  // ACTION EXECUTOR
  // =====================================================

  const executor =
    useActionExecutor()

  const runAction =

    executor?.runAction ??

    (async () => false)

  // =====================================================
  // PAGE STATE
  // =====================================================

  const pageReady =

    physicalTree?.kind === "layout" &&

    physicalTree.children.length > 0

  // =====================================================
  // CHROME
  // =====================================================

  const chrome =
    schema.chrome ?? {}

  const showFooter =
    chrome.footer !== false

  const showContainer =
    chrome.container !== false

  // =====================================================
  // CLASSES
  // =====================================================

  const pageClassName = [

    "page-container",

    chrome.fullscreen
      ? "page-fullscreen"
      : "",

    chrome.centered
      ? "page-centered"
      : "",

  ]
    .filter(Boolean)
    .join(" ")

  // =====================================================
  // CONTENT
  // =====================================================

  const content = (
    <>

      {schema.title && (
        <h1>{schema.title}</h1>
      )}

      {physicalTree && (
        <PhysicalRenderer
          node={physicalTree}
        />
      )}

      {showFooter &&
        pageReady &&
        actions.length > 0 && (

          <PageFooter
            actions={actions}
            run={runAction}
          />
      )}

    </>
  )

  // =====================================================
  // RENDER
  // =====================================================

  return (

    <div className={pageClassName}>

      {showContainer ? (

        <div className="ui-container">
          {content}
        </div>

      ) : (

        content

      )}

    </div>
  )
}