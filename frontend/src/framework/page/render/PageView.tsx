// src/framework/page/render/PageView.tsx

import { PhysicalRenderer }
  from "@/framework/physical/build/PhysicalRenderer"


import type { PhysicalNode }
  from "@/framework/physical/types/PhysicalNode"

import type { ApiPageSchema }
  from "../PageSchema"


export function PageView({
  schema,
  physicalTree,
}: {
  schema: ApiPageSchema
  physicalTree: PhysicalNode | null
}) {

  const chrome =
    schema.chrome ?? {}

  const showContainer =
    chrome.container !== false

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
    </>
  )

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