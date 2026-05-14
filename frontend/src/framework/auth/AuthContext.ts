// src/framework/auth/AuthContext.ts

import { createContext } from "react"

import type { Me }
  from "./auth"

import type { ActionResult }
  from "../api/action/types"

export type AuthContextType = {

  status:
    | "loading"
    | "anonymous"
    | "authenticated"

  me: Me | null

  refresh: () => Promise<void>

  logout: () => Promise<ActionResult>
}

export const AuthContext =
  createContext<AuthContextType | null>(
    null
  )