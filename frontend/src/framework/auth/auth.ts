export type Me = {
  authenticated: boolean

  id?: number
  username?: string
  email?: string
  role?: string | null // 👈 ДОБАВЬ

  permissions: string[] // 👈 лучше сделать обязательным
}