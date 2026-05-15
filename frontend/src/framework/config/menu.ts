// framework/config/menu.ts

export type MenuItem =
  | {
      label: string
      to: string
      permission?: string
    }
  | {
      label: string
      action: string
      permission?: string
    }

export const MENU: MenuItem[] = [

  {
    label: "Пользователи",
    to: "/page/user:list",
  },

  {
    label: "Роли",
    to: "/page/role:list",
  },

  {
    label: "Выйти",
    action: "logout",
  },

]