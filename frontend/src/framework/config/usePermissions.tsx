import { useAuth } from "../auth/AuthContext"

export function usePermissions() {
  const { me } = useAuth() // из /api/auth/me/

  return {
    has: (perm?: string) =>
      !perm || me?.permissions?.includes(perm),
  }
}
