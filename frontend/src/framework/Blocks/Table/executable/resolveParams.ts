// table/runtime/executable/resolveParams.ts

import type { BaseRow } from "../types/runtime"


type ParamValue =
  | string
  | number
  | boolean
  | null
  | undefined

type ParamsInput = Record<string, ParamValue>
type ParamsOutput = Record<string, ParamValue>

export function resolveParams<T extends BaseRow>(
  params: ParamsInput | undefined,
  row: T
): ParamsOutput {
  if (!params) {
    return {}
  }

  const result: ParamsOutput = {}

  for (const key in params) {
    const value = params[key]

    if (typeof value === "string") {
      if (value.startsWith("$row.")) {
        const field = value.replace("$row.", "")
        result[key] = row[field] as ParamValue
        continue
      }

      if (value === "$id") {
        result[key] =
          typeof row.id === "string" ||
          typeof row.id === "number"
            ? row.id
            : typeof row.pk === "string" ||
                typeof row.pk === "number"
              ? row.pk
              : typeof row.uuid === "string" ||
                  typeof row.uuid === "number"
                ? row.uuid
                : undefined

        continue
      }
    }

    result[key] = value
  }

  return result
}