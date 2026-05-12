// types.ts

// =========================
// AXIS
// =========================

export type MatrixAxisItem = {
  id: string
  label: string
}

// =========================
// CELL VALUE
// =========================

export type MatrixCellValue = {
  value?: string | number | null

  /**
   * domain-specific payload is allowed here,
   * because this is matrix data, not framework widget type.
   */
  attended?: boolean | null
  grade?: number | null
}

// =========================
// META
// =========================

export type MatrixMeta = {
  type: string
}

// =========================
// LAYOUT
// =========================

export type MatrixLayout = {
  x: MatrixAxisItem[]
  y: MatrixAxisItem[]
}

// =========================
// CAPABILITIES
// =========================

export type MatrixCapabilities = {
  view?: boolean
  edit?: boolean
}

// =========================
// PRESENTATION
// =========================

export type MatrixPresentationTone =
  | "neutral"
  | "success"
  | "warning"
  | "danger"
  | "info"
  | "accent"

export type MatrixPresentationEmphasis =
  | "soft"
  | "normal"
  | "strong"

export type MatrixPresentationMarker =
  | "active"
  | "muted"
  | "disabled"
  | "selected"

export type MatrixPresentationNode = {
  tone?: MatrixPresentationTone
  emphasis?: MatrixPresentationEmphasis
  marker?: MatrixPresentationMarker

  badge?: {
    text: string
    tone?: MatrixPresentationTone
  }

  icon?: string
}

// =========================
// SEMANTIC
// =========================

export type MatrixSemantic = {
  /**
   * examples:
   * - attendance_cell
   * - grade_cell
   * - schedule_cell
   */
  type: string
}

// =========================
// CELL SCHEMA
// =========================

export type MatrixPrimitiveWidget =
  | "select"
  | "number"
  | "text"

export type MatrixCellSchema = {
  /**
   * primitive fallback only.
   * domain widgets like "attendance" must not live here.
   */
  widget?: MatrixPrimitiveWidget

  /**
   * semantic renderer type.
   */
  semantic?: MatrixSemantic

  /**
   * visual metadata, not business state.
   */
  presentation?: MatrixPresentationNode

  choices?: {
    value: string | number
    label: string
  }[]

  readonly?: boolean
}

// =========================
// SCHEMA MAP
// =========================

export type MatrixSchema = {
  /**
   * default schema for all cells
   */
  defaultCell?: MatrixCellSchema

  /**
   * schema per exact cell key: `${x}:${y}`
   */
  cells?: Record<string, MatrixCellSchema>

  /**
   * schema per column/x id
   */
  columns?: Record<string, MatrixCellSchema>

  /**
   * schema per row/y id
   */
  rows?: Record<string, MatrixCellSchema>
}

// =========================
// DATA
// =========================

export type MatrixData = {
  meta: MatrixMeta
  layout: MatrixLayout
  cells: Record<string, MatrixCellValue>

  schema?: MatrixSchema

  presentation?: {
    cells?: Record<string, MatrixPresentationNode>
    rows?: Record<string, MatrixPresentationNode>
    columns?: Record<string, MatrixPresentationNode>
  }

  capabilities?: MatrixCapabilities
}

// =========================
// CHANGE
// =========================

export type MatrixChange = {
  x: string
  y: string
  value: MatrixCellValue
}