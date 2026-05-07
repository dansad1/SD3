// table/runtime/executable/types.ts

export type ExecutableAction = {
  key?: string

  to?: string
  action?: string

  params?: Record<string, unknown>
  ctx?: Record<string, unknown>

  confirm?:
    | boolean
    | {
        message?: string
      }

  reloadOnSuccess?: boolean
}