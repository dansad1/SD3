// components/widgets/BlockToolbar/BlockToolbar.tsx

import Button from "../ui/Button"
import Input from "../ui/Input"
import type { ToolbarAction } from "./toolbar"

interface BlockToolbarProps {
  actions?: ToolbarAction[]
  onAction?: (action: ToolbarAction) => void

  search?: {
    value: string
    onChange: (v: string) => void
    placeholder?: string
  }

  rightSlot?: React.ReactNode
}

export function BlockToolbar({
  actions = [],
  onAction,
  search,
  rightSlot,
}: BlockToolbarProps) {
  const sortedActions = [...actions].sort(
    (a, b) => (a.order ?? 0) - (b.order ?? 0)
  )

  if (!sortedActions.length && !search && !rightSlot) return null

  return (
    <div className="ui-list-toolbar">
      {sortedActions.length > 0 && (
        <div className="ui-list-toolbar__left">
          {sortedActions.map((action, index) => (
            <Button
              key={index}
              disabled={action.disabled}
              variant={index === 0 ? "primary" : "secondary"}
              size="sm"
              onClick={() => onAction?.(action)}
            >
              {action.label}
            </Button>
          ))}
        </div>
      )}

      {(search || rightSlot) && (
        <div className="ui-list-toolbar__right">
          {search && (
            <Input
              value={search.value}
              onChange={search.onChange}
              placeholder={search.placeholder ?? "Поиск…"}
            />
          )}
          {rightSlot}
        </div>
      )}
    </div>
  )
}