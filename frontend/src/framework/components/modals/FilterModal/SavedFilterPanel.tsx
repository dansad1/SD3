import Button from "../../ui/Button"

interface SavedFilter {
  id: number
  name: string
  query: Record<string, string | string[]>
}

export function SavedFiltersPanel({
  filters,
  onApply,
  onDelete,
}: {
  filters: SavedFilter[]
  onApply: (filter: SavedFilter) => void
  onDelete: (id: number) => void
}) {
  if (!filters.length) return null

  return (
    <div style={{ marginBottom: 16 }}>
      <b>Сохранённые фильтры:</b>

      <div style={{ display: "flex", flexDirection: "column", gap: 6, marginTop: 6 }}>
        {filters.map(sf => (
          <div
            key={sf.id}
            style={{ display: "flex", alignItems: "center", gap: 8 }}
          >
            <Button
              variant="ghost"
              onClick={() => onApply(sf)}
              style={{ flexGrow: 1, justifyContent: "flex-start" }}
            >
              {sf.name}
            </Button>

            <Button variant="danger" onClick={() => onDelete(sf.id)}>
              ✕
            </Button>
          </div>
        ))}
      </div>
    </div>
  )
}
