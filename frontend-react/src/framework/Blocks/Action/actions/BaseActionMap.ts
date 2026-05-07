// framework/action/baseActionMap.ts

import type { ActionMap } from "../types"
import { loginAction } from "./login"
import { logoutAction } from "./logout"

/**
 * Глобальные UI-действия.
 * Используются для клиентских сценариев, не требующих backend API.
 */
export const baseActionMap: ActionMap = {
  login: loginAction,
  logout: logoutAction,
}