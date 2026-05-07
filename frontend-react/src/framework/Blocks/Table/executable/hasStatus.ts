// table/runtime/executable/hasStatus.ts

export function hasStatus(
  value: unknown
): value is {
  status?: string
} {
  return (
    typeof value === "object" &&
    value !== null &&
    "status" in value
  )
}