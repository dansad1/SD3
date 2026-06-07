// src/framework/page/render/PageAreaLayout.tsx

import type {
  PhysicalLayoutNode,
} from "@/framework/physical/types/PhysicalNode"

import { splitAreaTree }
  from "./splitAreaTree"

import { PhysicalRenderer }
  from "@/framework/physical/build/PhysicalRenderer"

export function PageAreaLayout({
  root,
}: {
  root: PhysicalLayoutNode
}) {

  const areas =
    splitAreaTree(root)

  const hasLeft =
    areas["sidebar-left"].length > 0

  const hasRight =
    areas["sidebar-right"].length > 0

  const className = [

    "page-areas",

    hasLeft &&
      "page-areas-left",

    hasRight &&
      "page-areas-right",

  ]
    .filter(Boolean)
    .join(" ")

  return (

    <div className={className}>

      {hasLeft && (

        <aside
          className="page-sidebar-left"
        >

          {areas["sidebar-left"].map(
            (node, i) => (

              <PhysicalRenderer
                key={`left-${i}`}
                node={node}
              />

            )
          )}

        </aside>

      )}

      <main className="page-main">

        {areas.main.map(
          (node, i) => (

            <PhysicalRenderer
              key={`main-${i}`}
              node={node}
            />

          )
        )}

      </main>

      {hasRight && (

        <aside
          className="page-sidebar-right"
        >

          {areas["sidebar-right"].map(
            (node, i) => (

              <PhysicalRenderer
                key={`right-${i}`}
                node={node}
              />

            )
          )}

        </aside>

      )}

    </div>

  )
}