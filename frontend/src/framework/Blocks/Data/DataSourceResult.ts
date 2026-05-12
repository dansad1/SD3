export type DataSourceMeta = {
  page?: {
    page: number
    pages: number
    total: number
  }
  capabilities?: Record<string, unknown>
}

export type DataSourceResult<TData = unknown> = {
  data: TData

  loading: boolean
  error?: unknown

  reload: () => Promise<void>

  meta?: DataSourceMeta
}