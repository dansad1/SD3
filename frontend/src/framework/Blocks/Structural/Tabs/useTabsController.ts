import { useMemo, useState } from "react"
import type { TabsBlock } from "./types"
import type { ApiPageBlock } from "@/framework/page/PageSchema"
import { usePageApi } from "@/framework/page/context/usePageApi"
import { buildTabs } from "./tabsEngine"

type TabNode = ApiPageBlock & {
  blocks?: ApiPageBlock[]
  children?: ApiPageBlock[]
  title?: string
}

export function useTabsController(block: TabsBlock) {
  const page = usePageApi()
  const baseData = page.getData() as Record<string, unknown>

  const tabs = useMemo<TabNode[]>(
    () => buildTabs(block.blocks, baseData) as TabNode[],
    [block.blocks, baseData]
  )

  const [active, setActive] = useState(0)

  const safeActive =
    active >= 0 && active < tabs.length ? active : 0

  const current = tabs[safeActive]

  const content =
    current?.blocks ?? current?.children ?? []

  return {
    tabs,
    active: safeActive,
    setActive,
    content,
  }
}