import { useResolvedRuntimeProps } from "@/framework/bind/runtime/useResolvedRuntimeProps"
import type { BlockComponent } from "../../Registry/BlockRegistry"

import { InsertVariablesView } from "./InsertVariablesView"
import type {
  InsertVariableGroup,
  InsertVariableItem,
  InsertVariablesBlockType,
  InsertVariablesResponse,
} from "./types"

import { useActionExecutor } from "../../Action/executor/useActionExecutor"
import { useDataSource } from "../../Data/useDataSource"

/* ================= HELPERS ================= */

function formatValue(
  value: string,
  format: "template" | "raw" | "dollar" = "template"
) {
  if (format === "raw") return value
  if (format === "dollar") return `\${${value}}`
  return `{{ ${value} }}`
}

/* ================= COMPONENT ================= */

export const InsertVariablesBlock: BlockComponent<"insert_variables"> = ({
  block,
}) => {
  const runtime =
    useResolvedRuntimeProps(block) as InsertVariablesBlockType

  const { runAction } = useActionExecutor()

  /* ================= DATA ================= */

  const { data, loading } =
    useDataSource<InsertVariablesResponse>({
      data: runtime.source, // ✅ НИКАКОГО $
    })

  const groups: InsertVariableGroup[] =
    Array.isArray(data?.groups) ? data.groups : []

  const title =
    typeof data?.title === "string"
      ? data.title
      : "Доступные переменные"

  const onInsert = data?.onInsert

  /* ================= ACTION ================= */

  const handleInsert = (item: InsertVariableItem) => {
    const raw = item.value ?? item.key
    const formatted = formatValue(raw, runtime.format)

    // ✅ если action есть → через runtime
    if (onInsert?.type) {
      runAction(onInsert.type, {
        payload: {
          ...onInsert.payload,
          value: formatted,
          item,
        },
      })
      return
    }

    // ✅ fallback (чтобы блок работал без action вообще)
    window.dispatchEvent(
      new CustomEvent("form:setValue", {
        detail: {
          field: runtime.targetField,
          value: formatted,
          mode: "append",
        },
      })
    )
  }

  /* ================= DEBUG ================= */

  console.log("INSERT VARIABLES DATA", {
    source: runtime.source,
    data,
    loading,
  })

  /* ================= RENDER ================= */

  return (
    <InsertVariablesView
      groups={groups}
      loading={loading}
      onInsert={handleInsert}
      title={title}
    />
  )
}