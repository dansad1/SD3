import type {
  MatrixChange,
} from "@/framework/Blocks/Matrix/types"

import { api } from "../client"


export function submitMatrix(
  code: string,
  changes: MatrixChange[],
  context?: Record<string, unknown>,
): Promise<void> {

  return api.post(

    `/matrix/${code}/submit/`,

    {

      changes,

      context,

    },

  )

}