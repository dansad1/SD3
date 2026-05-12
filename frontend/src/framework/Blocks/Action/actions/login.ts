// framework/action/actions/login.ts

import { api } from "@/framework/api/сlient"
import type { ActionHandler } from "../types"

export const loginAction: ActionHandler = async (ctx) => {
  if (!ctx.data) return false

  await api.post("/auth/login/", ctx.data)
  return true
}