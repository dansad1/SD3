import type {
  BaseBlock,
} from "../BlockType"


export type StatusFlowBlock =
  BaseBlock & {
    type: "status_flow"

    source: string

    editable?: boolean
  }


export type Role = {
  id: number
  name: string
}


export type Target = {
  id: number
  name: string

  transitionId:
    | number
    | null

  roleIds: number[]
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


export type StatusFlowChange = {
  sourceId: number
  targetId: number
  roleId: number
  enabled: boolean
}


export type StatusFlowVM = {
  data:
    | StatusFlowData
    | null

  loading: boolean
  saving: boolean

  dirty: boolean
  editable: boolean

  error:
    | string
    | null

  toggleRole: (
    sourceStatusId: number,
    targetStatusId: number,
    role: Role,
    enabled: boolean,
  ) => void

  submit: () => Promise<void>

  reload: () => void
}