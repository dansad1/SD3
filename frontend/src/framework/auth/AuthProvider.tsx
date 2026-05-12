import { useEffect, useState, useCallback } from "react"
import { AuthContext } from "./AuthContext"
import type { Me } from "./auth"
import { loadMe } from "../api/authApi"
import { submitAction } from "../api/action/submitAction"

type AuthState =
  | { status: "loading" }
  | { status: "anonymous" }
  | { status: "authenticated"; me: Me }

type AppEffect = {
  type: string
  [key: string]: unknown
}

export function AuthProvider({
  children,
}: {
  children: React.ReactNode
}) {
  const [state, setState] = useState<AuthState>({
    status: "loading",
  })

  /* =========================
     REFRESH
  ========================= */

  const refresh = useCallback(async () => {
    try {
      const me = await loadMe()

      if (!me?.authenticated) {
        setState({ status: "anonymous" })
        return
      }

      setState({
        status: "authenticated",
        me,
      })
    } catch {
      setState({ status: "anonymous" })
    }
  }, [])

  /* =========================
     LOGOUT
  ========================= */

  const logout = useCallback(async () => {
    const res = await submitAction("auth.logout", {}) // 🔥 всегда {}
    await refresh() // 🔥 обновили auth state
    return res      // 🔥 вернули результат (для redirect)
  }, [refresh])

  /* =========================
     INITIAL LOAD
  ========================= */

  useEffect(() => {
    let mounted = true

    ;(async () => {
      if (!mounted) return
      await refresh()
    })()

    return () => {
      mounted = false
    }
  }, [refresh])

  /* =========================
     EFFECTS LISTENER
  ========================= */

  useEffect(() => {
    const handler = async (e: Event) => {
      const event = e as CustomEvent<AppEffect>

      if (event.detail?.type === "auth.reload_user") {
        await refresh()
      }
    }

    window.addEventListener("app:effect", handler)

    return () => {
      window.removeEventListener("app:effect", handler)
    }
  }, [refresh])

  /* =========================
     CONTEXT
  ========================= */

  return (
    <AuthContext.Provider
      value={{
        status: state.status,
        me:
          state.status === "authenticated"
            ? state.me
            : null,
        refresh,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}