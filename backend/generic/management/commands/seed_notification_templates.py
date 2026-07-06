# backend/project/notifications/management/commands/seed_notification_templates.py

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
      <h2 style="margin: 0; font-size: 20px;">
        {{ title }}
      </h2>
    </div>

    <div style="padding: 24px; color: #111827;">
      {{ content|safe }}

      <div style="
          margin-top: 24px;
          padding: 16px;
          background: #f9fafb;
          border-radius: 10px;
      ">
        <p style="margin: 0 0 8px;">
          <b>Заявка:</b> #{{ ticket.id }} — {{ ticket.title }}
        </p>
        <p style="margin: 0 0 8px;">
          <b>Статус:</b> {{ ticket.status }}
        </p>
        <p style="margin: 0;">
          <a href="{{ site_url }}/tickets/{{ ticket.id }}"
             style="
                 display: inline-block;
                 margin-top: 12px;
                 background: #2563eb;
                 color: #ffffff;
                 text-decoration: none;
                 padding: 10px 16px;
                 border-radius: 8px;
             ">
            Открыть заявку
          </a>
        </p>
      </div>
    </div>

    <div style="
        padding: 16px 24px;
        color: #6b7280;
        font-size: 12px;
        border-top: 1px solid #e5e7eb;
    ">
      Это автоматическое уведомление servicedesk.
    </div>
  </div>
</div>
"""


def html(title, content):
    return BASE_STYLE.replace(
        "{{ title }}",
        title,
    ).replace(
        "{{ content|safe }}",
        content,
    )


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
            {
                "code": "assigned_by_requester",
                "name": "Назначение заявителем",
                "subject": "Вас назначили по заявке #{{ ticket.id }}",
                "body": html(
                    "Вас назначили исполнителем",
                    """
                    <p>Здравствуйте, {{ user.full_name }}.</p>
                    <p>
                      Заявитель назначил вас исполнителем по заявке.
                      Посмотрите, пожалуйста, что там за радость.
                    </p>
                    """,
                ),
            },
            {
                "code": "ticket_changed",
                "name": "Изменение заявки",
                "subject": "Изменена заявка #{{ ticket.id }}",
                "body": html(
                    "Заявка изменена",
                    """
                    <p>В заявке появились изменения.</p>
                    <p>{{ changed_by.full_name }} обновил данные заявки.</p>
                    """,
                ),
            },
            {
                "code": "comment_created",
                "name": "Новый комментарий",
                "subject": "Новый комментарий в заявке #{{ ticket.id }}",
                "body": html(
                    "Новый комментарий",
                    """
                    <p><b>{{ comment.author.full_name }}</b> оставил комментарий:</p>
                    <blockquote style="
                        margin: 16px 0;
                        padding: 12px 16px;
                        background: #f3f4f6;
                        border-left: 4px solid #2563eb;
                    ">
                      {{ comment.text }}
                    </blockquote>
                    """,
                ),
            },
            {
                "code": "executors_changed",
                "name": "Изменение исполнителей",
                "subject": "Изменились исполнители заявки #{{ ticket.id }}",
                "body": html(
                    "Изменились исполнители",
                    """
                    <p>Список исполнителей был обновлён.</p>
                    <p>Проверьте, не попали ли вы в эту прекрасную компанию.</p>
                    """,
                ),
            },
            {
                "code": "watchers_changed",
                "name": "Изменение наблюдателей",
                "subject": "Изменились наблюдатели заявки #{{ ticket.id }}",
                "body": html(
                    "Изменились наблюдатели",
                    """
                    <p>Список наблюдателей по заявке был изменён.</p>
                    """,
                ),
            },
            {
                "code": "approvers_changed",
                "name": "Изменение согласующих",
                "subject": "Изменились согласующие заявки #{{ ticket.id }}",
                "body": html(
                    "Изменились согласующие",
                    """
                    <p>Список согласующих был обновлён.</p>
                    <p>Если вы среди них — пора согласовывать.</p>
                    """,
                ),
            },
            {
                "code": "executor_group_changed",
                "name": "Изменение группы исполнителей",
                "subject": "Изменилась группа исполнителей заявки #{{ ticket.id }}",
                "body": html(
                    "Группа исполнителей изменена",
                    """
                    <p>Заявка передана другой группе исполнителей.</p>
                    """,
                ),
            },
            {
                "code": "execution_expired",
                "name": "Просрочено исполнение",
                "subject": "Просрочено исполнение заявки #{{ ticket.id }}",
                "body": html(
                    "Срок исполнения истёк",
                    """
                    <p style="color: #b91c1c;">
                      Ай-ай-ай. Срок исполнения заявки истёк.
                    </p>
                    <p>Надо посмотреть и решить, пока оно не стало легендой.</p>
                    """,
                ),
            },
            {
                "code": "reaction_expired",
                "name": "Просрочена реакция",
                "subject": "Просрочена реакция на заявку #{{ ticket.id }}",
                "body": html(
                    "Срок реакции истёк",
                    """
                    <p style="color: #b91c1c;">
                      По заявке не было реакции в установленный срок.
                    </p>
                    """,
                ),
            },
            {
                "code": "approved",
                "name": "Заявка согласована",
                "subject": "Заявка #{{ ticket.id }} согласована",
                "body": html(
                    "Заявка согласована",
                    """
                    <p>Хорошие новости: заявка согласована.</p>
                    <p>Можно двигаться дальше.</p>
                    """,
                ),
            },
            {
                "code": "rated",
                "name": "Оценка заявки",
                "subject": "Заявитель оценил заявку #{{ ticket.id }}",
                "body": html(
                    "Получена оценка",
                    """
                    <p>Заявитель поставил оценку: <b>{{ rating.value }}</b>.</p>
                    <p>{{ rating.comment }}</p>
                    """,
                ),
            },
        ]

        for item in templates:
            template, created = (
                NotificationTemplate.objects
                .update_or_create(
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