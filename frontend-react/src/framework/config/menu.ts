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
    permission: "view_users",
  },
  {
    label: "Дисциплины",
    to: "/page/discipline:list",
    permission: "view_disciplines",
  },
  {
    label: "Расписание",
    to: "/page/schedule:week",
    permission: "view_schedule",
  },
  {
    label: "Журнал",
    to: "/page/journal:overview",
    permission: "view_journal",
  },
  {
    label: "Бэкапы",
    to: "/page/backup:list",
    permission: "view_backups", // 🔥 было без прав — теперь правильно
  },
  {
    label: "Роли",
    to: "/page/role:list",
    permission: "manage_roles",
  },
  {
    label: "Уведомления",
    to: "/page/notification_template:list",
    permission: "view_notifications",
  },
  {
    label: "Сообщения",
    to: "/page/message_center",
    permission: "view_messages", // 🔥 добавили
  },
  {
    label: "Мой профиль",
    to: "/page/user:profile",
    permission: "edit_self", // 🔥 логичнее, чем открытый доступ
  },

  {
    label: "Выйти",
    action: "auth.logout",
    // permission не нужен
  },
]