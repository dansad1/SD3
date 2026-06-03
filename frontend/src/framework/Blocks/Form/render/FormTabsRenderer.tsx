import { useState } from "react"

import {
  isSectionBlock,
  type FormBlock,
  type FormTabsBlock,
} from "../types/types"

type Props = {
  block: FormTabsBlock

  render: (
    block: FormBlock
  ) => React.ReactNode
}

export function FormTabsRenderer({
  block,
  render,
}: Props) {

  const sections =
    block.children.filter(
      isSectionBlock
    )

  const [active, setActive] =
    useState(0)

  if (
    sections.length === 0
  ) {
    return null
  }

  return (
    <div
      className={`ui-tabs ui-tabs-${
        block.variant ?? "line"
      }`}
      style={{
        gridColumn: `span ${block.layout?.span ?? 12}`,
        order: block.layout?.order,
      }}
    >

      <div className="ui-tabs-header align-start">

        {sections.map(
          (
            section,
            index
          ) => (
            <button
              key={section.id}
              type="button"
              className={`ui-tab ${
                index === active
                  ? "active"
                  : ""
              }`}
              onClick={() =>
                setActive(index)
              }
            >
              {section.title ??
                `Tab ${index + 1}`}
            </button>
          )
        )}

      </div>

      <div className="ui-tabs-body">
        {render(
          sections[active]
        )}
      </div>

    </div>
  )
}