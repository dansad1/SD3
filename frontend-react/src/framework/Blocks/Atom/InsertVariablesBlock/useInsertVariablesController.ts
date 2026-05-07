import { useActionExecutor } from "../../Action/executor/useActionExecutor"
import { useDataSource } from "../../Data/useDataSource"
import type { InsertVariableItem, InsertVariablesResponse } from "./types"

/* ================= TYPES ================= */


type Props = {
  source: string
  format?: "template" | "raw" | "dollar"
}

/* ================= HELPERS ================= */

function formatValue(
  value: string,
  format: "template" | "raw" | "dollar" = "template"
) {
  if (format === "raw") return value
  if (format === "dollar") return `\${${value}}`
  return `{{ ${value} }}`
}

/* ================= CONTROLLER ================= */

export function useInsertVariablesController(props: Props) {
  const { source, format = "template" } = props

  const { runAction } = useActionExecutor()

  const { data, loading } = useDataSource<InsertVariablesResponse>({
    data: `$${source}`,
  })

  const groups = data?.groups ?? []
  const title = data?.title
  const onInsert = data?.onInsert

  const handleInsert = (item: InsertVariableItem) => {
    if (!onInsert) return

    const raw = item.value ?? item.key
    const formatted = formatValue(raw, format)

    runAction(onInsert.type, {
      payload: {
        ...onInsert.payload,
        value: formatted,
        item,
      },
    })
  }

  return {
    groups,
    loading,
    handleInsert,
    title,
  }
}