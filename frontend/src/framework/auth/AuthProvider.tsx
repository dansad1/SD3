// src/framework/auth/AuthProvider.tsx

import {
  useEffect,
  useState,
  useCallback,
} from "react"

import { AuthContext }
  from "./AuthContext"

import type { Me }
  from "./auth"

import { loadMe }
  from "../api/authApi"

import { submitAction }
  from "../api/action/submitAction"

type AuthState =

  | {
      status: "loading"
    }

  | {
      status: "anonymous"
    }

  | {
      status: "authenticated"
      me: Me
    }

export function AuthProvider({
  children,
}: {
  children: React.ReactNode
}) {

  /* ================================================== */
  /* STATE */
  /* ================================================== */

  const [state, setState] =
    useState<AuthState>({
      status: "loading",
    })

  /* ================================================== */
  /* REFRESH */
  /* ================================================== */

  const refresh =
    useCallback(async () => {

      console.log(
        "🔄 AUTH REFRESH"
      )

      try {

        const me =
          await loadMe()

        console.log(
          "👤 ME RESPONSE",
          me
        )

        if (!me?.authenticated) {

          setState({
            status: "anonymous",
          })

          return
        }

        setState({

          status: "authenticated",

          me,

        })

      } catch (e) {

        console.error(
          "❌ AUTH REFRESH ERROR",
          e
        )

        setState({
          status: "anonymous",
        })
      }

    }, [])

  /* ================================================== */
  /* GLOBAL AUTH REF */
  /* ================================================== */

  useEffect(() => {

    ;(window as any).__refreshAuth =
      refresh

    return () => {

      delete (window as any)
        .__refreshAuth
    }

  }, [refresh])

  /* ================================================== */
  /* LOGOUT */
  /* ================================================== */

  const logout =
    useCallback(async () => {

      const result =
        await submitAction(
          "logout",
          {}
        )

      // fallback
      await refresh()

      return result

    }, [refresh])

  /* ================================================== */
  /* INITIAL LOAD */
  /* ================================================== */

  useEffect(() => {

    let mounted = true

    ;(async () => {

      if (!mounted) {
        return
      }

      await refresh()

    })()

    return () => {

      mounted = false
    }

  }, [refresh])

  /* ================================================== */
  /* CONTEXT */
  /* ================================================== */

  return (

    <AuthContext.Provider

      value={{

        status:
          state.status,

        me:

          state.status ===
          "authenticated"

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