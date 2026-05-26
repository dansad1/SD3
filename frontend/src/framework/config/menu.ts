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
    label: "Заявки",
    to: "/page/ticket:list",
  },

  {
    label: "База знаний",
    to: "/page/knowledge_article:list",
  },

  {
    label: "Компании",
    to: "/page/company:list",
  },

  {
    label: "Пользователи",
    to: "/page/user:list",
  },

  {
    label: "Роли",
    to: "/page/role:list",
  },

  {
    label: "Настройки",
    to: "/page/settings:home",
  },

  {
    label: "CMDB",
    to: "/page/ci_type:list",
  },

  {
    label: "Аналитика",
    to: "/page/analytics_report:list",
  },

  {
    label: "Сервисы",
    to: "/page/service:list",
  },

  {
    label: "Выход",
    action: "logout",
  },
]