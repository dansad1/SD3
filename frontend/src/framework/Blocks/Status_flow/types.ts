import type { BaseBlock } from "../BlockType"
// ======================================
// DSL
// ======================================

export type StatusFlowBlock = BaseBlock & {
  type: "status_flow"
  source: string
  params?: Record<string, unknown>
  editable?: boolean

}


// ======================================
// Resource
// ======================================

export type Role = {
  id: number
  name: string

}


export type Target = {
  id: number
  name: string
  roles: string[]

}


export type Status = {
  id: number
  name: string
  color: string
  targets: Target[]

}


export type StatusFlowData = {
  roles: Role[]
  statuses: Status[]

}


// ======================================
// VM
// ======================================

export type StatusFlowVM = {
  data: StatusFlowData | null
  loading: boolean
  error: string | null

}