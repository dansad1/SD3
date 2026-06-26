import { getWidgetDefinition } from "@/framework/components/dynamic/widgets/helpers"

const GRID = 12

export type FieldLayout = {
  preferredSpan?: number
  grow?: boolean
}

export type FormField = {
  name?: string
  type?: string
  widget?: string
  layout?: FieldLayout
}

export type BalancedField = {
  field: FormField
  span: number
}

export type BalancedRow = BalancedField[]

function preferred(field: FormField): number {
  const widget = getWidgetDefinition(field.widget)

  return (
    field.layout?.preferredSpan ??
    widget?.layout.preferredSpan ??
    6
  )
}

function growable(field: FormField): boolean {
  const widget = getWidgetDefinition(field.widget)

  return (
    field.layout?.grow ??
    widget?.layout.grow ??
    true
  )
}

export function balanceRowsProcessor(
  fields: FormField[]
): BalancedRow[] {
  const rows: BalancedRow[] = []

  let row: BalancedRow = []
  let total = 0

  for (const field of fields) {
    const span = preferred(field)

    if (row.length && total + span > GRID) {
      rows.push(distribute(row))
      row = []
      total = 0
    }

    row.push({
      field,
      span,
    })

    total += span
  }

  if (row.length) {
    rows.push(distribute(row))
  }

  return rows
}

function distribute(row: BalancedRow): BalancedRow {
  let free =
    GRID -
    row.reduce(
      (sum: number, item: BalancedField) =>
        sum + item.span,
      0
    )

  const candidates = row.filter(
    (item: BalancedField) => growable(item.field)
  )

  while (free > 0 && candidates.length) {
    for (const item of candidates) {
      if (free === 0) {
        break
      }

      item.span += 1
      free -= 1
    }
  }

  return row
}