import type { MatrixData } from "@/framework/Blocks/Matrix/types"
import { api } from "../client"

export function loadMatrix(
  code: string,
  ctx?: Record<string, unknown>
): Promise<MatrixData> {
  const query = ctx
    ? `?ctx=${encodeURIComponent(JSON.stringify(ctx))}`
    : ""

  return api.get<MatrixData>(`/matrix/${code}/${query}`)
}