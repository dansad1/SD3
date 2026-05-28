// src/routes/AppRoutes.tsx

import {
  Routes,
  Route,
  Navigate,
  useParams,
} from "react-router-dom"

import { useContext } from "react"

import {
  AuthContext,
} from "@/framework/auth/AuthContext"

import SchemaRoute
  from "./SchemaRoute"

import { PAGES }
  from "@/Project/pages"

/* ===================================================== */
/* PROTECTED PAGE ROUTE */
/* ===================================================== */

function ProtectedPageRoute() {

  const auth =
    useContext(AuthContext)

  const {
    code = "login",
  } = useParams<{
    code?: string
  }>()

  /* =================================================== */
  /* AUTH NOT READY */
  /* =================================================== */

  if (
    !auth ||
    auth.status === "loading"
  ) {

    return null
  }

  /* =================================================== */
  /* PAGE */
  /* =================================================== */

  const page =
    PAGES[code]

  if (!page) {

    return (
      <div>
        Страница не найдена: {code}
      </div>
    )
  }

  /* =================================================== */
  /* AUTH META */
  /* =================================================== */

  /*
    По умолчанию:
    ВСЕ страницы приватные
  */

  const authRequired =
    page.auth !== false

  /*
    Только для гостей:
    login/register/reset
  */

  const guestOnly =
    page.guestOnly === true

  /* =================================================== */
  /* PRIVATE PAGE */
  /* =================================================== */

  if (
    authRequired &&
    auth.status !==
      "authenticated"
  ) {

    return (
      <Navigate
        to="/page/login"
        replace
      />
    )
  }

  /* =================================================== */
  /* GUEST ONLY */
  /* =================================================== */

  if (
    guestOnly &&
    auth.status ===
      "authenticated"
  ) {

    return (
      <Navigate
        to="/"
        replace
      />
    )
  }

  /* =================================================== */
  /* OK */
  /* =================================================== */

  return <SchemaRoute />
}

/* ===================================================== */
/* APP ROUTES */
/* ===================================================== */

export default function AppRoutes() {

  const auth =
    useContext(AuthContext)

  /* =================================================== */
  /* WAIT AUTH */
  /* =================================================== */

  if (
    !auth ||
    auth.status === "loading"
  ) {

    return null
  }

  /* =================================================== */
  /* ROUTES */
  /* =================================================== */

  return (

    <Routes>

      {/* ============================================= */}
      {/* ROOT */}
      {/* ============================================= */}

      <Route

        path="/"

        element={

          auth.status ===
          "authenticated"

            ? (

              <Navigate
                to="/page/user:list"
                replace
              />

            ) : (

              <Navigate
                to="/page/login"
                replace
              />

            )
        }
      />

      {/* ============================================= */}
      {/* LEGACY LOGIN */}
      {/* ============================================= */}

      <Route

        path="/login"

        element={

          <Navigate
            to="/page/login"
            replace
          />

        }
      />

      {/* ============================================= */}
      {/* GENERIC PAGE ROUTE */}
      {/* ============================================= */}

      <Route

        path="/page/:code"

        element={
          <ProtectedPageRoute />
        }

      />

      {/* ============================================= */}
      {/* 404 */}
      {/* ============================================= */}

      <Route

        path="*"

        element={

          <Navigate
            to="/"
            replace
          />

        }

      />

    </Routes>

  )
}