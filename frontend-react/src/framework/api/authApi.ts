// src/framework/api/authApi.ts

import type { Me } from "../auth/auth"



export async function loadMe(): Promise<Me> {
  const res = await fetch("/api/me/", {
    method: "GET",
    credentials: "include",
  })

  if (!res.ok) {
    return {
      authenticated: false,
      permissions: [],
    }
  }

  const data = await res.json()

  return {
    authenticated: data.authenticated,

    id: data.user?.id,
    username: data.user?.username,
    email: data.user?.email,
    role: data.user?.role,

    permissions: data.permissions ?? [],
  }
}