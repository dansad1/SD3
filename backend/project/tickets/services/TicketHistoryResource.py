from ast import literal_eval
from datetime import (
    date,
    datetime,
)
from decimal import Decimal
from json import loads
from uuid import UUID

from django.db.models import Model
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.html import strip_tags

from backend.project.audit.resources.EntityHistoryResource import (
    EntityHistoryResource,
)
from backend.project.tickets.models import (
    TicketAttachment,
    TicketComment,
)
from backend.project.tickets.services.TicketCommentService import (
    TicketCommentService,
)


class TicketHistoryResource(
    EntityHistoryResource,
):

    code = "ticket.history"

    ENTITY = "tickets"

    ACTION_FIELDS = {
        "status": {
            "status",
        },
        "assign": {
            "executor",
            "executors",
            "assignee",
            "assignees",
            "assigned_to",
            "executor_group",
        },
        "sla": {
            "due_date",
            "deadline",
            "sla",
        },
        "priority": {
            "priority",
        },
        "type": {
            "type",
            "service",
        },
        "archive": {
            "archived",
        },
    }

    ACTION_TITLES = {
        "create": "Заявка создана",
        "update": "Изменены поля",
        "status": "Статус изменён",
        "assign": "Изменено назначение",
        "sla": "Изменён срок",
        "priority": "Изменён приоритет",
        "type": "Изменён тип заявки",
        "archive": "Изменено состояние архива",
        "comment": "Добавлен комментарий",
        "attachment": "Добавлено вложение",
        "delete": "Заявка удалена",
        "email": "Отправлено письмо",
        "system": "Системное событие",
    }

    ACTION_ORDER = (
        "status",
        "assign",
        "sla",
        "priority",
        "type",
        "archive",
    )

    SERVICE_FIELDS = {
        "comment",
        "attachment",
        "attachments",
        "lifecycle",
    }

    # =====================================================
    # COMMON SERIALIZATION
    # =====================================================

    def serialize_datetime(
        self,
        value,
    ):
        if value is None:
            return None

        if (
            isinstance(value, datetime)
            and timezone.is_aware(value)
        ):
            value = timezone.localtime(
                value,
            )

        return value.isoformat()

    def serialize_actor(
        self,
        actor,
    ):
        if actor is None:
            return None

        return {
            "id": getattr(
                actor,
                "pk",
                None,
            ),
            "label": force_str(
                actor,
            ),
        }

    def serialize_text(
        self,
        value,
    ):
        return strip_tags(
            force_str(
                value
                or "",
            )
        ).strip()

    def get_choice_label(
        self,
        field,
        value,
    ):
        if field is None:
            return None

        choices = (
            getattr(
                field,
                "choices",
                None,
            )
            or getattr(
                field,
                "options",
                None,
            )
            or []
        )

        if isinstance(
            choices,
            dict,
        ):
            choices = choices.items()

        for choice in choices:
            if isinstance(
                choice,
                dict,
            ):
                choice_value = choice.get(
                    "value",
                )
                choice_label = (
                    choice.get(
                        "label",
                    )
                    or choice.get(
                        "title",
                    )
                    or choice.get(
                        "name",
                    )
                )
            elif (
                isinstance(
                    choice,
                    (list, tuple),
                )
                and len(choice) >= 2
            ):
                choice_value = choice[0]
                choice_label = choice[1]
            else:
                continue

            if str(choice_value) == str(value):
                return force_str(
                    choice_label,
                )

        return None

    def serialize_value(
        self,
        field,
        value,
    ):
        if value in (
            None,
            "",
        ):
            return "—"

        if value is True:
            return "Да"

        if value is False:
            return "Нет"

        if isinstance(
            value,
            Model,
        ):
            return force_str(
                value,
            )

        if isinstance(
            value,
            datetime,
        ):
            return self.serialize_datetime(
                value,
            )

        if isinstance(
            value,
            date,
        ):
            return value.isoformat()

        if isinstance(
            value,
            dict,
        ):
            label = (
                value.get(
                    "label",
                )
                or value.get(
                    "title",
                )
                or value.get(
                    "text",
                )
                or value.get(
                    "name",
                )
            )

            if label not in (
                None,
                "",
            ):
                return self.serialize_text(
                    label,
                )

            nested_value = (
                value.get(
                    "value",
                )
                if "value" in value
                else value.get(
                    "id",
                )
            )

            if nested_value not in (
                None,
                "",
            ):
                choice_label = self.get_choice_label(
                    field,
                    nested_value,
                )

                return (
                    choice_label
                    or force_str(
                        nested_value,
                    )
                )

            return "—"

        if isinstance(
            value,
            (list, tuple, set),
        ):
            serialized = [
                self.serialize_value(
                    field,
                    item,
                )
                for item in value
            ]

            serialized = [
                item
                for item in serialized
                if item != "—"
            ]

            return (
                ", ".join(
                    serialized,
                )
                or "—"
            )

        choice_label = self.get_choice_label(
            field,
            value,
        )

        if choice_label:
            return choice_label

        if isinstance(
            value,
            (Decimal, UUID),
        ):
            return str(
                value,
            )

        return self.serialize_text(
            value,
        )

    # =====================================================
    # AUDIT CHANGES
    # =====================================================

    def normalize_changes(
        self,
        fields,
        raw_changes,
    ):
        result = {}

        for index, change in enumerate(
            raw_changes or [],
        ):
            field_name = force_str(
                (
                    change.get(
                        "field",
                    )
                    or change.get(
                        "name",
                    )
                    or f"change-{index}"
                )
            )

            if field_name in self.SERVICE_FIELDS:
                continue

            field = fields.get(
                field_name,
            )

            before = (
                change.get(
                    "old_value",
                )
                if "old_value" in change
                else change.get(
                    "before",
                )
            )

            after = (
                change.get(
                    "new_value",
                )
                if "new_value" in change
                else change.get(
                    "after",
                )
            )

            if before == after:
                continue

            result[field_name] = {
                "label": self.get_field_label(
                    field_name,
                    field,
                    change,
                ),
                "before": self.serialize_value(
                    field,
                    before,
                ),
                "after": self.serialize_value(
                    field,
                    after,
                ),
                "fieldType": (
                    change.get(
                        "field_type",
                    )
                    or change.get(
                        "fieldType",
                    )
                    or getattr(
                        field,
                        "type",
                        None,
                    )
                ),
            }

        return result

    def split_changes(
        self,
        changes,
    ):
        groups = {}
        remaining = dict(
            changes,
        )

        for action in self.ACTION_ORDER:
            field_names = self.ACTION_FIELDS[
                action
            ]

            action_changes = {
                name: remaining.pop(
                    name,
                )
                for name in tuple(
                    remaining,
                )
                if name in field_names
            }

            if action_changes:
                groups[action] = action_changes

        if remaining:
            groups["update"] = remaining

        return groups

    def get_stored_action(
        self,
        item,
    ):
        action = getattr(
            item,
            "action",
            None,
        )

        if action:
            return force_str(
                action,
            )

        return force_str(
            (
                item.meta
                or {}
            ).get(
                "action",
                "",
            )
        )

    def build_event_meta(
        self,
        item,
        action,
    ):
        meta = dict(
            item.meta
            or {},
        )

        meta.pop(
            "changes",
            None,
        )

        meta["title"] = self.ACTION_TITLES.get(
            action,
            "Изменение заявки",
        )

        return meta

    def build_audit_events(
        self,
        *,
        item,
        ticket,
        fields,
    ):
        stored_action = self.get_stored_action(
            item,
        )

        item_meta = (
            item.meta
            or {}
        )

        if (
            stored_action == "create"
            or item_meta.get(
                "mode",
            ) == "create"
        ):
            return []

        raw_changes = self.get_raw_changes(
            item,
        )

        changes = self.normalize_changes(
            fields,
            raw_changes,
        )

        if changes:
            groups = self.split_changes(
                changes,
            )
        elif stored_action in {
            "delete",
            "email",
            "system",
        }:
            groups = {
                stored_action: {},
            }
        else:
            return []

        result = []

        for action, action_changes in groups.items():
            result.append({
                "id": (
                    f"audit-{item.pk}-{action}"
                ),
                "type": action,
                "action": action,
                "created": (
                    self.serialize_datetime(
                        item.created,
                    )
                ),
                "actor": self.serialize_actor(
                    item.actor,
                ),
                "object_repr": (
                    self.get_object_repr(
                        item,
                        ticket,
                        ticket.pk,
                    )
                ),
                "changes": action_changes,
                "meta": self.build_event_meta(
                    item,
                    action,
                ),
            })

        return result

    # =====================================================
    # CREATE
    # =====================================================

    def build_create_event(
        self,
        ticket,
    ):
        actor = None

        for name in (
            "created_by",
            "requester",
        ):
            try:
                actor = ticket.get_value(
                    name,
                )
            except (
                AttributeError,
                ValueError,
            ):
                actor = None

            if actor is not None:
                break

        return {
            "id": f"ticket-{ticket.pk}-create",
            "type": "create",
            "action": "create",
            "created": self.serialize_datetime(
                ticket.created_at,
            ),
            "actor": self.serialize_actor(
                actor,
            ),
            "object_repr": force_str(
                ticket,
            ),
            "changes": {},
            "meta": {
                "title": self.ACTION_TITLES[
                    "create"
                ],
                "text": "Заявка была создана.",
            },
        }

    # =====================================================
    # COMMENTS
    # =====================================================

    def serialize_comment_text(
        self,
        value,
    ):
        if isinstance(
            value,
            dict,
        ):
            return self.serialize_text(
                value.get(
                    "text",
                    "",
                )
            )

        text = force_str(
            value
            or "",
        )

        if (
            text.startswith(
                "{",
            )
            and text.endswith(
                "}",
            )
        ):
            try:
                legacy_value = loads(
                    text,
                )
            except ValueError:
                try:
                    legacy_value = literal_eval(
                        text,
                    )
                except (
                    SyntaxError,
                    ValueError,
                ):
                    legacy_value = None

            if isinstance(
                legacy_value,
                dict,
            ):
                return self.serialize_text(
                    legacy_value.get(
                        "text",
                        text,
                    )
                )

        return self.serialize_text(
            text,
        )

    def get_comment_events(
        self,
        request,
        ticket,
    ):
        queryset = (
            TicketComment.objects
            .filter(
                ticket=ticket,
            )
            .select_related(
                "author",
                "edited_by",
            )
            .order_by(
                "-created_at",
            )
        )

        queryset = (
            TicketCommentService
            .filter_queryset(
                queryset,
                request.user,
            )
        )

        events = []

        for item in queryset:
            can_manage = (
                request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or item.author_id
                    == request.user.pk
                )
            )

            edited = bool(
                item.edited_at,
            )

            events.append({
                "id": f"comment-{item.pk}",
                "type": "comment",
                "action": "comment",
                "created": (
                    self.serialize_datetime(
                        item.created_at,
                    )
                ),
                "actor": self.serialize_actor(
                    item.author,
                ),
                "object_repr": None,
                "changes": {},
                "meta": {
                    "id": item.pk,
                    "title": (
                        "Комментарий изменён"
                        if edited
                        else self.ACTION_TITLES[
                            "comment"
                        ]
                    ),
                    "text": (
                        self.serialize_comment_text(
                            item.text,
                        )
                    ),
                    "hidden": (
                        item.hide_from_client
                    ),
                    "edited": edited,
                    "edited_at": (
                        self.serialize_datetime(
                            item.edited_at,
                        )
                    ),
                    "edited_by": (
                        self.serialize_actor(
                            item.edited_by,
                        )
                    ),
                    "can_edit": can_manage,
                    "can_delete": can_manage,
                },
            })

        return events

    # =====================================================
    # ATTACHMENTS
    # =====================================================

    def get_attachment_events(
        self,
        ticket,
    ):
        queryset = (
            TicketAttachment.objects
            .filter(
                ticket=ticket,
            )
            .select_related(
                "uploaded_by",
                "stored_file",
                "field",
            )
            .order_by(
                "-created_at",
            )
        )

        events = []

        for item in queryset:
            stored_file = getattr(
                item,
                "stored_file",
                None,
            )

            events.append({
                "id": f"attachment-{item.pk}",
                "type": "attachment",
                "action": "attachment",
                "created": (
                    self.serialize_datetime(
                        item.created_at,
                    )
                ),
                "actor": self.serialize_actor(
                    item.uploaded_by,
                ),
                "object_repr": None,
                "changes": {},
                "meta": {
                    "id": item.pk,
                    "title": self.ACTION_TITLES[
                        "attachment"
                    ],
                    "text": (
                        item.original_name
                        if stored_file
                        else "Файл недоступен"
                    ),
                    "size": (
                        item.size
                        if stored_file
                        else 0
                    ),
                    "mime_type": (
                        item.mime_type
                        if stored_file
                        else ""
                    ),
                    "field": (
                        {
                            "id": item.field_id,
                            "label": force_str(
                                item.field,
                            ),
                        }
                        if item.field
                        else None
                    ),
                },
            })

        return events

    # =====================================================
    # RESOURCE
    # =====================================================

    def get(
        self,
        request,
        **params,
    ):
        ticket_id = params.get(
            "id",
        )

        if not ticket_id:
            return []

        entity = self.get_entity(
            self.ENTITY,
        )

        entity.check_permission(
            request,
            "view",
        )

        ticket = (
            entity.get_queryset(
                request,
            )
            .filter(
                pk=ticket_id,
            )
            .first()
        )

        if ticket is None:
            return []

        fields = self.get_field_map(
            request=request,
            entity_obj=entity,
            instance=ticket,
        )

        journal_queryset = (
            self.get_journal_queryset(
                ticket,
            )
        )

        events = [
            self.build_create_event(
                ticket,
            ),
        ]

        for item in journal_queryset:
            events.extend(
                self.build_audit_events(
                    item=item,
                    ticket=ticket,
                    fields=fields,
                )
            )

        events.extend(
            self.get_comment_events(
                request,
                ticket,
            )
        )

        events.extend(
            self.get_attachment_events(
                ticket,
            )
        )

        events.sort(
            key=lambda event: (
                event.get(
                    "created",
                )
                or ""
            ),
            reverse=True,
        )

        return events

    def get_journal_queryset(
        self,
        ticket,
    ):
        from backend.project.audit.models.EntityJournal import (
            EntityJournal,
        )

        return (
            EntityJournal.objects
            .filter(
                entity=self.ENTITY,
                object_id=str(
                    ticket.pk,
                ),
            )
            .select_related(
                "actor",
            )
            .order_by(
                "-created",
            )
        )