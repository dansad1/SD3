// framework/action/actions/logout.ts

import { api } from "@/framework/api/сlient"
import type { ActionHandler } from "../types"

export const logoutAction: ActionHandler = async () => {
  await api.post("/auth/logout/")
  window.location.href = "/login"
  return true
}