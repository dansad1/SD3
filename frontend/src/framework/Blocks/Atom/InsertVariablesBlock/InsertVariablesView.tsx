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
      <div className="w-full rounded-xl border bg-neutral-50 p-6 text-sm text-neutral-500">
        Загрузка...
      </div>
    )
  }

  if (!groups.length) {
    return (
      <div className="w-full rounded-xl border bg-neutral-50 p-6 text-sm text-neutral-500">
        Нет переменных
      </div>
    )
  }

  return (

    <div className="w-full rounded-xl border bg-neutral-50 p-6">

      <div className="mb-6 text-lg font-semibold">
        {title ?? "Доступные переменные"}
      </div>

      <div className="space-y-6">

        {groups.map(group => (

          <div
            key={group.key}
          >

            <div className="mb-3 text-sm font-semibold text-neutral-700">
              {group.label}
            </div>

            <div className="flex flex-wrap gap-x-3 gap-y-3">

              {group.items.map(item => (

                <Button
                  key={item.key}
                  size="sm"
                  variant="primary"
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