export type TraceStatus = "running" | "ok" | "error"

export type TraceTrigger =
  | "mount"
  | "action"
  | "submit"
  | "load"
  | "request"

export type TraceMeta = {
  page?: string
  entity?: string
  block?: string
  action?: string
  field?: string
  api?: string
  method?: string
  mode?: "create" | "edit" | "view"
  objectId?: string | number
  message?: string
  error?: string
  [key: string]: unknown
}

export type TraceStep = {
  id: string
  name: string
  status: TraceStatus
  meta?: TraceMeta
  startedAt: number
  finishedAt?: number
  children: TraceStep[]
}

export type TraceRecord = {
  id: string
  page: string
  trigger: TraceTrigger
  status: Exclude<TraceStatus, "running">
  startedAt: number
  finishedAt: number
  root: TraceStep
  summary: string
}

export type TraceSnapshot = {
  records: TraceRecord[]
  errors: TraceRecord[]
  last?: TraceRecord
  lastError?: TraceRecord
}