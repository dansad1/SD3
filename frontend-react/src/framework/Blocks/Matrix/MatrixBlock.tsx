import { useMatrix } from "./runtime/useMatrix"
import { MatrixGrid } from "./MatrixGrid"
import { usePageRuntimeContext } from "@/framework/page/runtime/usePageRuntimeContext"
import { resolveObject } from "@/framework/bind/expression/resolveUnified"


type Props = {
  code: string
  context?: Record<string, unknown>
    params?: Record<string, unknown> // 👈 ДОБАВЬ

}

export const MatrixBlock = ({ code, context, params }: Props) => {
  const runtimeCtx = usePageRuntimeContext()

  const raw = params || context

  const resolvedContext = raw
    ? resolveObject(raw, runtimeCtx)
    : raw

  console.log("MATRIX RAW:", raw)
  console.log("MATRIX RESOLVED:", resolvedContext)

  const { data, updateCell } = useMatrix(code, resolvedContext)

  if (!data) return <div>Loading...</div>

  return (
    <MatrixGrid
      layout={data.layout}
      cells={data.cells}
      onChange={updateCell}
    />
  )
}