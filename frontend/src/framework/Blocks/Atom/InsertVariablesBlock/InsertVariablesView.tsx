import Button from "@/framework/components/ui/Button"
import type {
  InsertVariableItem,
  InsertVariableGroup,
} from "./types"

type Props = {
  groups: InsertVariableGroup[]
  loading: boolean
  onInsert: (item: InsertVariableItem) => void
  title?: string
}

export function InsertVariablesView({
  groups,
  loading,
  onInsert,
  title,
}: Props) {
  if (loading) {
    return (
      <div className="p-4 text-sm text-neutral-500">
        Загрузка...
      </div>
    )
  }

  if (!groups.length) {
    return (
      <div className="p-4 text-sm text-neutral-500">
        Нет переменных
      </div>
    )
  }

  return (
    <div className="p-4 border rounded-xl bg-neutral-50">
      <div className="mb-4 font-semibold">
        {title || "Доступные переменные"}
      </div>

      <div className="flex flex-col gap-4">
        {groups.map(group => (
          <div key={group.key}>
            <div className="mb-2 text-sm font-medium">
              {group.label}
            </div>

            <div className="flex flex-wrap gap-2">
              {group.items.map(item => (
                <Button
                  key={item.key}
                  size="sm"
                  onClick={() => onInsert(item)}
                >
                  {item.label}
                </Button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}