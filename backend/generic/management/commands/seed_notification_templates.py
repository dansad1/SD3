


from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import transaction


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

      <div style="
          margin-top:24px;
          padding:16px;
          background:#f9fafb;
          border-radius:10px;
      ">
        <p><b>Заявка:</b> #{{ ticket.id }} — {{ ticket.title }}</p>

        <p><b>Статус:</b> {{ ticket.status }}</p>

        <p><b>Изменения:</b></p>

        {{ changes_html|safe }}

        <p style="margin-top:16px;">
          <a
            href="{{ site_url }}/tickets/{{ ticket.id }}"
            style="
                display:inline-block;
                background:#2563eb;
                color:#fff;
                text-decoration:none;
                padding:10px 16px;
                border-radius:8px;
            "
          >
            Открыть заявку
          </a>
        </p>
      </div>

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


def html(title, content):
    return (
        BASE_STYLE
        .replace("{{ title }}", title)
        .replace("{{ content|safe }}", content)
    )


class Command(BaseCommand):

    help = "Seed notification templates"

    @transaction.atomic
    def handle(self, *args, **options):

        NotificationTemplate = apps.get_model(
            "notifications",
            "NotificationTemplate",
        )

        changed_body = html(
            "Заявка изменена",
            """
            <p>
                Заявка была обновлена.
            </p>

            <p>
                Ниже приведен список измененных полей.
            </p>
            """,
        )

        templates = [

            # =====================================================
            # TICKET
            # =====================================================

            {
                "code": "ticket.created",
                "name": "Создание заявки",
                "subject": "Создана заявка #{{ ticket.id }}",
                "body": html(
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
                "subject": "Изменена заявка #{{ ticket.id }}",
                "body": changed_body,
            },

            {
                "code": "ticket.closed",
                "name": "Заявка закрыта",
                "subject": "Заявка #{{ ticket.id }} закрыта",
                "body": html(
                    "Заявка закрыта",
                    """
                    <p>
                        Работа по заявке завершена.
                    </p>
                    """,
                ),
            },

            # =====================================================
            # COMMENTS
            # =====================================================

            {
                "code": "ticket.comment_added",
                "name": "Комментарий",
                "subject": "Новый комментарий в заявке #{{ ticket.id }}",
                "body": html(
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

            # =====================================================
            # APPROVAL
            # =====================================================

            {
                "code": "ticket.approved",
                "name": "Заявка согласована",
                "subject": "Заявка #{{ ticket.id }} согласована",
                "body": html(
                    "Заявка согласована",
                    """
                    <p>
                        Заявка успешно согласована.
                    </p>
                    """,
                ),
            },

            # =====================================================
            # SLA
            # =====================================================

            {
                "code": "ticket.execution_expired",
                "name": "Просрочено исполнение",
                "subject": "Просрочено исполнение заявки #{{ ticket.id }}",
                "body": html(
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
                "subject": "Просрочена реакция по заявке #{{ ticket.id }}",
                "body": html(
                    "Просрочена реакция",
                    """
                    <p style="color:#b91c1c;">
                        Истек срок реакции по заявке.
                    </p>
                    """,
                ),
            },

            # =====================================================
            # FEEDBACK
            # =====================================================

            {
                "code": "ticket.rated",
                "name": "Получена оценка",
                "subject": "Получена оценка по заявке #{{ ticket.id }}",
                "body": html(
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

        ]

        for item in templates:

            template, created = (
                NotificationTemplate.objects.update_or_create(
                    code=item["code"],
                    defaults={
                        "name": item["name"],
                        "channels": ["email"],
                        "subject": item["subject"],
                        "body": item["body"],
                        "is_active": True,
                    },
                )
            )

            self.stdout.write(
                f"{'🟢' if created else '✔'} {template.code}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Notification templates synchronized."
            )
        )