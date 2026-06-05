export type Me = {
  authenticated: boolean

  id?: number
  username?: string
  email?: string
  role?: string | null // 👈 ДОБАВЬ
capabilities: Record<
    string,
    boolean
  >
  permissions: string[] // 👈 лучше сделать обязательным
}