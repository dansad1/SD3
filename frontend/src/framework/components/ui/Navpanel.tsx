import { useContext } from "react"
import { NavLink, useNavigate } from "react-router-dom"
import { AuthContext } from "@/framework/auth/AuthContext"
import { MENU } from "@/framework/config/menu"
import type { MenuItem } from "@/framework/config/menu"
import { submitAction } from "@/framework/api/action/submitAction"

function filterMenu(menu: MenuItem[], permissions: string[]) {
  return menu.filter((item) => {
    if (!item.permission) return true
    return permissions.includes(item.permission)
  })
}

function isLink(item: MenuItem): item is Extract<MenuItem, { to: string }> {
  return "to" in item
}

export function NavPanel() {

  const auth =
    useContext(AuthContext)

  const navigate =
    useNavigate()

  if (!auth || auth.status === "loading") {
    return null
  }

  if (auth.status !== "authenticated") {
    return null
  }

  // 🔥 ВОТ ЭТОГО НЕ ХВАТАЛО
  const { logout } = auth

  const permissions =
    auth.me?.permissions ?? []

  const items =
    filterMenu(
      MENU,
      permissions
    )

  const handleAction = async (
    item: Extract<
      MenuItem,
      { action: string }
    >
  ) => {

    /* ====================================== */
    /* LOGOUT */
    /* ====================================== */

    if (
      item.action === "logout"
    ) {

      await logout()

      return
    }

    /* ====================================== */
    /* GENERIC ACTION */
    /* ====================================== */

    const res =
      await submitAction(
        item.action,
        {}
      )

    if (res?.redirect) {

      navigate(
        "/page/" +
        res.redirect
      )
    }
  }

  return (

    <nav className="nav-panel">

      {/* ================================== */}
      {/* MENU */}
      {/* ================================== */}

      <div className="nav-left">

        <ul className="nav-list">

          {items.map((item) => (

            <li key={item.label}>

              {isLink(item)

                ? (

                  <NavLink
                    to={item.to}

                    className={({
                      isActive
                    }) =>

                      isActive

                        ? "nav-link active"

                        : "nav-link"
                    }
                  >

                    {item.label}

                  </NavLink>

                ) : (

                  <button

                    onClick={() =>
                      handleAction(item)
                    }

                    className="
                      nav-link
                      nav-button
                    "
                  >

                    {item.label}

                  </button>

                )}

            </li>

          ))}

        </ul>

      </div>

      {/* ================================== */}
      {/* USER */}
      {/* ================================== */}

      <div className="nav-right">

        <div className="nav-user">

          <div className="nav-user-name">

            {auth.me?.username}

          </div>

          <div className="nav-user-meta">

            {auth.me?.email}

          </div>

        </div>

      </div>

    </nav>
  )
}