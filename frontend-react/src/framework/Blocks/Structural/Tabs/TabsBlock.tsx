import { TabsView } from "./TabsView."
import type { TabsBlock } from "./types"
import { useTabsController } from "./useTabsController"

export function TabsBlock({ block }: { block: TabsBlock }) {
  const ctrl = useTabsController(block)

  return (
    <TabsView
      tabs={ctrl.tabs}
      active={ctrl.active}
      onChange={ctrl.setActive}
      content={ctrl.content}
      variant={block.variant}
      align={block.align}
    />
  )
}