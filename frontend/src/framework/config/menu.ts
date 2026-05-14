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
    label: "Выйти",
    action: "logout",
    // permission не нужен
  },
]