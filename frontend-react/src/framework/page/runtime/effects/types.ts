export type EffectToastVariant =
  | "success"
  | "error"
  | "info"
  | "warning"

export type ToastEffect = {
  type: "toast"
  message: string
  variant?: EffectToastVariant
}

export type NavigateEffect = {
  type: "navigate"
  page: string
}

export type ReloadEffect = {
  type: "reload"
  target: string
}

export type SetDataEffect = {
  type: "set_data"
  key: string
  value: unknown
}

export type EmitEffect = {
  type: "emit"
  event: string
  payload?: unknown
}

export type CloseModalEffect = {
  type: "close_modal"
}

export type OpenModalEffect = {
  type: "open_modal"
  modal: string
  payload?: unknown
}

/* ================= AUTH ================= */

export type AuthReloadUserEffect = {
  type: "auth.reload_user"
}

/* ================= UNION ================= */

export type PageEffect =
  | ToastEffect
  | NavigateEffect
  | ReloadEffect
  | SetDataEffect
  | EmitEffect
  | CloseModalEffect
  | OpenModalEffect
  | AuthReloadUserEffect

/* ================= DEPS ================= */

export type RunEffectsDeps = {
  navigate: (page: string) => void
  setDataKey: (
    key: string,
    value: unknown
  ) => void
  emit: (
    event: string,
    payload?: unknown
  ) => void
  toast?: (
    message: string,
    variant?: EffectToastVariant
  ) => void
}