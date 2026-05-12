// src/framework/Blocks/Chat/features/useChatNavigation.ts

import { useNavigate, useLocation } from "react-router-dom"

export function useChatNavigation() {
  const navigate = useNavigate()
  const location = useLocation()

  function openChat(id: string | number, selectedId: string) {
    if (String(id) === selectedId) return

    const params = new URLSearchParams(location.search)
    params.set("id", String(id))

    navigate(
      {
        pathname: location.pathname,
        search: params.toString(),
      },
      {
        replace: false, // можно true если не хочешь засорять history
      }
    )
  }

  return {
    openChat,
  }
}