from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction


# =========================================================
# BASE LAYOUT
# =========================================================

BASE_STYLE = """
<div style="
    font-family: Arial, sans-serif;
    background: #f6f8fb;
    padding: 24px;
">
  <div style="
      max-width: 680px;
      margin: 0 auto;
      background: #ffffff;
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid #e5e7eb;
  ">
    <div style="
        background: #1f2937;
        color: #ffffff;
        padding: 20px 24px;
    ">
      <h2 style="margin:0;font-size:20px;">
        {{ title }}
      </h2>
    </div>

    <div style="padding:24px;color:#111827;">

      {{ content|safe }}

      {{ details|safe }}

    </div>

    <div style="
        padding:16px 24px;
        color:#6b7280;
        font-size:12px;
        border-top:1px solid #e5e7eb;
    ">
      Это автоматическое уведомление ServiceDesk.
    </div>

  </div>
</div>
"""


# =========================================================
# DETAILS
# =========================================================

TICKET_DETAILS = """
<div style="
    margin-top:24px;
    padding:16px;
    background:#f9fafb;
    border-radius:10px;
">
  <p style="margin:0 0 12px;">
    <b>Заявка:</b>
    #{{ ticket.id }}
    {% if ticket_name %}
      — {{ ticket_name }}
    {% endif %}
  </p>

  <p style="margin:0 0 12px;">
    <b>Статус:</b>
    {% if ticket_status %}
      {{ ticket_status }}
    {% else %}
      Не указан
    {% endif %}
  </p>

  <p style="margin:0 0 8px;">
    <b>Изменения:</b>
  </p>

  {% if changes_html %}
    {{ changes_html|safe }}
  {% else %}
    <p style="
        margin:0;
        color:#6b7280;
    ">
      Нет данных об изменениях.
    </p>
  {% endif %}

  <p style="margin:16px 0 0;">
    <a
      href="{{ site_url }}/tickets/{{ ticket.id }}"
      style="
          display:inline-block;
          background:#2563eb;
          color:#ffffff;
          text-decoration:none;
          padding:10px 16px;
          border-radius:8px;
      "
    >
      Открыть заявку
    </a>
  </p>
</div>
"""

USER_DETAILS = """
<div style="
    margin-top:24px;
    padding:16px;
    background:#f9fafb;
    border-radius:10px;
">
  <p>
    <b>Пользователь:</b>
    {{ user }}
  </p>

  <p>
    <b>Логин:</b>
    {{ user.login }}
  </p>

  <p>
    <b>Роль:</b>
    {{ user.role }}
  </p>

  <p>
    <b>Активен:</b>

    {% if user.is_active %}
      Да
    {% else %}
      Нет
    {% endif %}
  </p>

  {% if changes_html %}
    <p>
      <b>Изменения:</b>
    </p>

    {{ changes_html|safe }}
  {% endif %}

  <p style="margin-top:16px;">
    <a
      href="{{ site_url }}/users/{{ user.id }}"
      style="
          display:inline-block;
          background:#2563eb;
          color:#ffffff;
          text-decoration:none;
          padding:10px 16px;
          border-radius:8px;
      "
    >
      Открыть пользователя
    </a>
  </p>
</div>
"""


# =========================================================
# BUILDERS
# =========================================================

def html(
    title,
    content,
    details="",
):
    return (
        BASE_STYLE
        .replace(
            "{{ title }}",
            title,
        )
        .replace(
            "{{ content|safe }}",
            content,
        )
        .replace(
            "{{ details|safe }}",
            details,
        )
    )


def ticket_html(
    title,
    content,
):
    return html(
        title=title,
        content=content,
        details=TICKET_DETAILS,
    )


def user_html(
    title,
    content,
):
    return html(
        title=title,
        content=content,
        details=USER_DETAILS,
    )


# =========================================================
# COMMAND
# =========================================================

class Command(BaseCommand):

    help = "Seed notification templates"

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ):

        NotificationTemplate = apps.get_model(
            "notifications",
            "NotificationTemplate",
        )

        templates = [

            # =================================================
            # TICKET
            # =================================================

            {
                "code": "ticket.created",
                "name": "Создание заявки",
                "subject": (
                    "Создана заявка "
                    "#{{ ticket.id }}"
                ),
                "body": ticket_html(
                    "Создана новая заявка",
                    """
                    <p>
                      Создана новая заявка.
                    </p>
                    """,
                ),
            },

            {
                "code": "ticket.changed",
                "name": "Изменение заявки",
                "subject": (
                    "Изменена заявка "
                    "#{{ ticket.id }}"
                ),
                "body": ticket_html(
                    "Заявка изменена",
                    """
                    <p>
                      Заявка была обновлена.
                    </p>

                    <p>
                      Ниже приведен список измененных полей.
                    </p>
                    """,
                ),
            },

            {
                "code": "ticket.closed",
                "name": "Заявка закрыта",
                "subject": (
                    "Заявка "
                    "#{{ ticket.id }} закрыта"
                ),
                "body": ticket_html(
                    "Заявка закрыта",
                    """
                    <p>
                      Работа по заявке завершена.
                    </p>
                    """,
                ),
            },

            # =================================================
            # COMMENTS
            # =================================================

            {
                "code": "ticket.comment_added",
                "name": "Комментарий",
                "subject": (
                    "Новый комментарий в заявке "
                    "#{{ ticket.id }}"
                ),
                "body": ticket_html(
                    "Добавлен комментарий",
                    """
                    <p>
                      Добавлен новый комментарий.
                    </p>

                    <blockquote
                      style="
                          margin:16px 0;
                          padding:12px 16px;
                          background:#f3f4f6;
                          border-left:4px solid #2563eb;
                      "
                    >
                      {{ comment.text }}
                    </blockquote>
                    """,
                ),
            },

            # =================================================
            # APPROVAL
            # =================================================

            {
                "code": "ticket.approved",
                "name": "Заявка согласована",
                "subject": (
                    "Заявка "
                    "#{{ ticket.id }} согласована"
                ),
                "body": ticket_html(
                    "Заявка согласована",
                    """
                    <p>
                      Заявка успешно согласована.
                    </p>
                    """,
                ),
            },

            # =================================================
            # SLA
            # =================================================

            {
                "code": "ticket.execution_expired",
                "name": "Просрочено исполнение",
                "subject": (
                    "Просрочено исполнение заявки "
                    "#{{ ticket.id }}"
                ),
                "body": ticket_html(
                    "Просрочено исполнение",
                    """
                    <p style="color:#b91c1c;">
                      Истек срок исполнения заявки.
                    </p>
                    """,
                ),
            },

            {
                "code": "ticket.reaction_expired",
                "name": "Просрочена реакция",
                "subject": (
                    "Просрочена реакция по заявке "
                    "#{{ ticket.id }}"
                ),
                "body": ticket_html(
                    "Просрочена реакция",
                    """
                    <p style="color:#b91c1c;">
                      Истек срок реакции по заявке.
                    </p>
                    """,
                ),
            },

            # =================================================
            # FEEDBACK
            # =================================================

            {
                "code": "ticket.rated",
                "name": "Получена оценка",
                "subject": (
                    "Получена оценка по заявке "
                    "#{{ ticket.id }}"
                ),
                "body": ticket_html(
                    "Получена оценка",
                    """
                    <p>
                      Заявитель оценил выполнение заявки.
                    </p>

                    <p>
                      <b>Оценка:</b>
                      {{ rating.value }}
                    </p>

                    {% if rating.comment %}
                      <p>
                        <b>Комментарий:</b><br>
                        {{ rating.comment }}
                      </p>
                    {% endif %}
                    """,
                ),
            },

            # =================================================
            # USERS
            # =================================================

            {
                "code": "user.created",
                "name": "Создание пользователя",
                "subject": (
                    "Создан пользователь "
                    "{{ user.login }}"
                ),
                "body": user_html(
                    "Создан пользователь",
                    """
                    <p>
                      В ServiceDesk создан новый пользователь.
                    </p>

                    {% if actor %}
                      <p>
                        <b>Создал:</b>
                        {{ actor }}
                      </p>
                    {% endif %}
                    """,
                ),
            },

            {
                "code": "user.changed",
                "name": "Изменение пользователя",
                "subject": (
                    "Изменен пользователь "
                    "{{ user.login }}"
                ),
                "body": user_html(
                    "Пользователь изменен",
                    """
                    <p>
                      Данные пользователя были изменены.
                    </p>

                    {% if actor %}
                      <p>
                        <b>Изменил:</b>
                        {{ actor }}
                      </p>
                    {% endif %}
                    """,
                ),
            },

            {
                "code": "user.activated",
                "name": "Активация пользователя",
                "subject": (
                    "Пользователь "
                    "{{ user.login }} активирован"
                ),
                "body": user_html(
                    "Пользователь активирован",
                    """
                    <p>
                      Учетная запись пользователя активирована.
                    </p>

                    {% if actor %}
                      <p>
                        <b>Активировал:</b>
                        {{ actor }}
                      </p>
                    {% endif %}
                    """,
                ),
            },

            {
                "code": "user.deactivated",
                "name": "Деактивация пользователя",
                "subject": (
                    "Пользователь "
                    "{{ user.login }} деактивирован"
                ),
                "body": user_html(
                    "Пользователь деактивирован",
                    """
                    <p>
                      Учетная запись пользователя деактивирована.
                    </p>

                    {% if actor %}
                      <p>
                        <b>Деактивировал:</b>
                        {{ actor }}
                      </p>
                    {% endif %}
                    """,
                ),
            },

            {
                "code": "user.role_changed",
                "name": "Изменение роли пользователя",
                "subject": (
                    "Изменена роль пользователя "
                    "{{ user.login }}"
                ),
                "body": user_html(
                    "Роль пользователя изменена",
                    """
                    <p>
                      Пользователю назначена новая роль.
                    </p>

                    {% if actor %}
                      <p>
                        <b>Изменил:</b>
                        {{ actor }}
                      </p>
                    {% endif %}
                    """,
                ),
            },

            {
                "code": "user.password_changed",
                "name": "Изменение пароля пользователя",
                "subject": (
                    "Изменен пароль пользователя "
                    "{{ user.login }}"
                ),
                "body": user_html(
                    "Пароль пользователя изменен",
                    """
                    <p>
                      Пароль учетной записи был изменен.
                    </p>

                    <p style="
                        color:#6b7280;
                        font-size:13px;
                    ">
                      Значение пароля в уведомлении не передается.
                    </p>

                    {% if actor %}
                      <p>
                        <b>Изменил:</b>
                        {{ actor }}
                      </p>
                    {% endif %}
                    """,
                ),
            },

            {
                "code": "user.deleted",
                "name": "Удаление пользователя",
                "subject": (
                    "Удален пользователь "
                    "{{ user.login }}"
                ),
                "body": user_html(
                    "Пользователь удален",
                    """
                    <p>
                      Пользователь был удален из ServiceDesk.
                    </p>

                    {% if actor %}
                      <p>
                        <b>Удалил:</b>
                        {{ actor }}
                      </p>
                    {% endif %}
                    """,
                ),
            },

        ]

        synced_codes = []

        for item in templates:

            synced_codes.append(
                item["code"],
            )

            template, created = (
                NotificationTemplate.objects
                .update_or_create(
                    code=item["code"],
                    defaults={
                        "name": item["name"],
                        "channels": [
                            "email",
                        ],
                        "subject": item["subject"],
                        "body": item["body"],
                        "is_active": True,
                    },
                )
            )

            self.stdout.write(
                f"{'🟢' if created else '✔'} "
                f"{template.code}"
            )

        deleted, _ = (
            NotificationTemplate.objects
            .exclude(
                code__in=synced_codes,
            )
            .delete()
        )

        if deleted:

            self.stdout.write(
                self.style.WARNING(
                    f"Удалено шаблонов: {deleted}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Notification templates synchronized."
            )
        )