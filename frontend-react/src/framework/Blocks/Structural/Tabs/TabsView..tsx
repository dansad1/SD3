import type { ApiPageBlock } from "@/framework/page/PageSchema"
import { BlockRenderer } from "../../Registry/BlockRenderer"

type TabNode = ApiPageBlock & {
  title?: string
}

export function TabsView({
  tabs,
  active,
  onChange,
  content,
  variant,
  align,
}: {
  tabs: TabNode[]
  active: number
  onChange: (i: number) => void
  content: ApiPageBlock[]
  variant?: string
  align?: string
}) {
  return (
    <div className={`ui-tabs ui-tabs-${variant ?? "line"}`}>
      <div className={`ui-tabs-header align-${align ?? "start"}`}>
        {tabs.map((tab, i) => (
          <button
            key={tab.id ?? `tab-${i}`}
            type="button"
            className={`ui-tab ${i === active ? "active" : ""}`}
            onClick={() => onChange(i)}
          >
            {tab.title || `Tab ${i + 1}`}
          </button>
        ))}
      </div>

      <div className="ui-tabs-body">
        {content.map((b, i) => (
          <BlockRenderer
            key={b.id ?? `block-${i}`}
            block={b}
          />
        ))}
      </div>
    </div>
  )
}