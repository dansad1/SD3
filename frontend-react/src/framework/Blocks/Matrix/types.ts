// types.ts

// =========================
// AXIS
// =========================

export type MatrixAxisItem = {
  id: string
  label: string
}

// =========================
// CELL VALUE (generic!)
// =========================

export type MatrixCellValue = {
  value?: string | number | null
  attended?: boolean | null
  grade?: number | null
}
export type MatrixMeta = {
  type: string
}

// =========================
// LAYOUT (структура)
// =========================

export type MatrixLayout = {
  x: MatrixAxisItem[]
  y: MatrixAxisItem[]
}

// =========================
// DATA
// =========================

export type MatrixData = {
  meta: MatrixMeta
  layout: MatrixLayout
  cells: Record<string, MatrixCellValue>

  capabilities?: {
    view?: boolean
    edit?: boolean
  }
}

// =========================
// CHANGE (submit)
// =========================

export type MatrixChange = {
  x: string
  y: string
  value: MatrixCellValue
}
export type MatrixCellSchema = {
  widget: "select" | "number" | "text" | "attendance"

  choices?: {
    value: string | number
    label: string
  }[]
}