import { Routes, Route, Navigate } from "react-router-dom"
import { useContext } from "react"
import { AuthContext } from "@/framework/auth/AuthContext"
import SchemaRoute from "./SchemaRoute"

export default function AppRoutes() {

  const auth = useContext(AuthContext)

  /* ================= LOADING ================= */

  if (!auth || auth.status === "loading") {
    return null
  }

  /* ================= ROUTES ================= */

  return (

    <Routes>

      {/* 🔐 LOGIN */}
      <Route
        path="/login"
        element={<SchemaRoute />}
      />

      {/* 🏠 ROOT */}
      <Route
        path="/"
        element={
          auth.status === "authenticated"

            ? (
              <Navigate
                to="/page/user:list"
                replace
              />
            )

            : (
              <Navigate
                to="/login"
                replace
              />
            )
        }
      />

      {/* 🔐 PROTECTED */}
      <Route
        path="/page/:code"
        element={

          auth.status === "authenticated"

            ? <SchemaRoute />

            : (
              <Navigate
                to="/login"
                replace
              />
            )
        }
      />

    </Routes>

  )
}