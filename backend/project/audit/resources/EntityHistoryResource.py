import logging
from typing import Any

from backend.engine.Resource.BaseResource import BaseResource
from backend.engine.entity.EntityRegistry import entity_registry
from backend.project.audit.models.EntityJournal import EntityJournal

logger = logging.getLogger(__name__)

HIDDEN_FIELDS = {
    "id",
    "pk",
    "created",
    "created_at",
    "updated",
    "updated_at",
    "deleted_at",
}


class EntityHistoryResource(BaseResource):
    code = "entity.history"

    # =====================================================
    # ENTITY / OBJECT
    # =====================================================

    def get_entity(self, entity_code):
        return entity_registry.get(entity_code)

    def get_instance(
            self,
            request,
            entity_obj,
            object_id,
    ):
        return (
            entity_obj.model.objects
            .filter(
                pk=object_id,
            )
            .first()
        )
    # =====================================================
    # FIELDS
    # =====================================================

    def get_field_map(
        self,
        request,
        entity_obj,
        instance,
    ):
        """
        BaseEntity.get_fields(request, obj=instance) уже объединяет:
        - DjangoField;
        - DynamicField.

        Передача instance нужна, чтобы TicketEntity выбрала
        динамический fieldset текущего типа заявки.
        """
        try:
            fields = entity_obj.get_fields(
                request=request,
                obj=instance,
            )
        except TypeError:
            # Совместимость со старыми Entity, где obj ещё не принят.
            fields = entity_obj.get_fields(
                request
            )

        return {
            field.name: field
            for field in (fields or [])
            if getattr(field, "name", None)
        }

    # =====================================================
    # RAW CHANGES
    # =====================================================

    def get_raw_changes(self, item):
        """
        Канонический источник — meta["changes"], потому что там есть:
        field, label, old_value, new_value, field_type, source.

        Для старых записей остаётся fallback на item.changes.
        """
        meta = item.meta or {}
        meta_changes = meta.get("changes")

        if isinstance(meta_changes, list):
            return [
                change
                for change in meta_changes
                if isinstance(change, dict)
            ]

        result = []

        for name, change in (
            item.changes or {}
        ).items():
            if not isinstance(change, dict):
                continue

            result.append(
                {
                    "field": name,
                    "label": change.get("label"),
                    "old_value": change.get(
                        "before",
                        change.get("old_value"),
                    ),
                    "new_value": change.get(
                        "after",
                        change.get("new_value"),
                    ),
                    "field_type": change.get(
                        "field_type",
                        change.get("fieldType"),
                    ),
                    "source": change.get("source"),
                }
            )

        return result

    # =====================================================
    # LABELS
    # =====================================================

    def get_field_label(
        self,
        field_name,
        field,
        change,
    ):
        label = getattr(
            field,
            "label",
            None,
        )

        if label:
            return str(label)

        explicit_label = change.get(
            "label"
        )

        if explicit_label:
            return str(explicit_label)

        return (
            str(field_name)
            .replace("_", " ")
            .capitalize()
        )

    # =====================================================
    # VALUE SERIALIZATION
    # =====================================================

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

        if isinstance(
                value,
                dict,
        ):
            return str(

                value.get("label")

                or value.get("text")

                or value.get("name")

                or value.get("value")

                or "—"

            )

        if isinstance(
                value,
                (
                        list,
                        tuple,
                        set,
                ),
        ):
            return ", ".join(

                str(
                    self.serialize_value(
                        field,
                        item,
                    )
                )

                for item in value

            )

        return str(value)
    def get_choice_label(
        self,
        field,
        value,
    ):
        choices = getattr(
            field,
            "choices",
            None,
        ) or []

        for choice in choices:
            if isinstance(choice, dict):
                choice_value = choice.get(
                    "value"
                )
                choice_label = choice.get(
                    "label"
                )
            elif (
                isinstance(choice, (list, tuple))
                and len(choice) >= 2
            ):
                choice_value = choice[0]
                choice_label = choice[1]
            else:
                continue

            if str(choice_value) == str(value):
                return str(choice_label)

        return None

    def format_value(
        self,
        value: Any,
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

        if isinstance(value, dict):
            label = value.get("label")

            if label not in (
                None,
                "",
            ):
                return str(label)

            return str(value)

        if isinstance(value, (list, tuple, set)):
            parts = [
                self.format_value(item)
                for item in value
            ]

            return ", ".join(parts)

        return str(value)

    # =====================================================
    # NORMALIZATION
    # =====================================================

    def normalize_changes(
        self,
        fields,
        raw_changes,
    ):
        result = {}

        for index, change in enumerate(
            raw_changes or []
        ):
            field_name = (
                change.get("field")
                or change.get("name")
                or f"change-{index}"
            )

            if field_name in HIDDEN_FIELDS:
                continue

            field = fields.get(
                field_name
            )

            before = (
                change.get("old_value")
                if "old_value" in change
                else change.get("before")
            )

            after = (
                change.get("new_value")
                if "new_value" in change
                else change.get("after")
            )

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
                    change.get("field_type")
                    or change.get("fieldType")
                    or getattr(field, "type", None)
                ),
            }

        return result

    # =====================================================
    # ACTION
    # =====================================================

    def detect_action(
        self,
        item,
        changes,
    ):
        stored_action = getattr(
            item,
            "action",
            None,
        )

        if stored_action in {
            "create",
            "delete",
            "comment",
            "attachment",
            "email",
            "system",
        }:
            return stored_action

        if len(changes) == 1:
            field_name = next(
                iter(changes)
            )

            if field_name == "status":
                return "status"

            if field_name in {
                "executor",
                "assignee",
                "assigned_to",
            }:
                return "assign"

        return "update"

    def get_action_title(
        self,
        action,
    ):
        return {
            "create": "Объект создан",
            "update": "Изменены поля",
            "delete": "Объект удалён",
            "status": "Статус изменён",
            "assign": "Изменён исполнитель",
            "comment": "Комментарий",
            "attachment": "Добавлено вложение",
            "email": "Отправлено письмо",
            "system": "Системное событие",
        }.get(
            action,
            "Изменение",
        )

    # =====================================================
    # META / REPRESENTATION
    # =====================================================

    def build_meta(
        self,
        item,
        action,
    ):
        meta = dict(
            item.meta or {}
        )

        # Эти изменения уже нормализованы в корневом changes.
        meta.pop(
            "changes",
            None,
        )

        meta["title"] = self.get_action_title(
            action
        )

        return meta

    def get_object_repr(
        self,
        item,
        instance,
        object_id,
    ):
        value = getattr(
            item,
            "object_repr",
            None,
        )

        if (
            not value
            or str(value) == str(object_id)
        ):
            return str(instance)

        return str(value)

    # =====================================================
    # HISTORY
    # =====================================================

    def get_history(
            self,
            request,
            entity,
            object_id,
            *,
            include_create=False,
    ):
        logger.info(
            "=== HISTORY %s:%s ===",
            entity,
            object_id,
        )

        entity_obj = self.get_entity(
            entity,
        )

        logger.info(
            "Entity: %s",
            entity_obj.__class__.__name__,
        )

        entity_obj.check_permission(
            request,
            "view",
        )

        instance = self.get_instance(
            request,
            entity_obj,
            object_id,
        )

        logger.info(
            "Instance: %r",
            instance,
        )

        if instance is None:
            logger.warning(
                "Instance not found"
            )
            return []

        fields = self.get_field_map(
            request=request,
            entity_obj=entity_obj,
            instance=instance,
        )

        logger.info(
            "Fields: %s",
            sorted(fields.keys()),
        )

        queryset = (

            EntityJournal.objects

            .filter(
                entity=entity,
                object_id=str(
                    object_id,
                ),
            )

            .select_related(
                "actor",
            )

            .order_by(
                "-created",
            )

        )

        logger.info(
            "Journal rows: %s",
            queryset.count(),
        )

        events = []

        for item in queryset:

            logger.info(
                "------------------------------------------------"
            )

            logger.info(
                "Journal id=%s created=%s",
                item.pk,
                item.created,
            )

            logger.info(
                "Meta=%s",
                item.meta,
            )

            logger.info(
                "Changes(raw)=%s",
                item.changes,
            )

            item_meta = (
                    item.meta
                    or {}
            )

            if (
                    not include_create
                    and (
                    getattr(
                        item,
                        "action",
                        None,
                    ) == "create"
                    or item_meta.get(
                "mode"
            ) == "create"
            )
            ):
                logger.info(
                    "Skip create event"
                )
                continue

            raw_changes = self.get_raw_changes(
                item,
            )

            logger.info(
                "Raw changes=%s",
                raw_changes,
            )

            changes = self.normalize_changes(
                fields,
                raw_changes,
            )

            logger.info(
                "Normalized changes=%s",
                changes,
            )

            action = self.detect_action(
                item,
                changes,
            )

            logger.info(
                "Detected action=%s",
                action,
            )

            if (
                    action == "update"
                    and not changes
            ):
                logger.warning(
                    "Skip empty update"
                )
                continue

            event = {

                "id":
                    item.pk,

                "action":
                    action,

                "created":
                    item.created.isoformat(),

                "actor":
                    (
                        {
                            "id":
                                item.actor_id,

                            "label":
                                str(item.actor),
                        }
                        if item.actor
                        else None
                    ),

                "object_repr":
                    self.get_object_repr(
                        item,
                        instance,
                        object_id,
                    ),

                "changes":
                    changes,

                "meta":
                    self.build_meta(
                        item,
                        action,
                    ),
            }

            logger.info(
                "Event=%s",
                event,
            )

            events.append(
                event,
            )

        logger.info(
            "History events=%s",
            len(events),
        )

        logger.info(
            "=== END HISTORY ==="
        )

        return events
    # =====================================================
    # RESOURCE
    # =====================================================

    def get(
        self,
        request,
        **params,
    ):
        entity = params.get(
            "entity"
        )

        object_id = params.get(
            "id"
        )

        if (
            not entity
            or not object_id
        ):
            return []

        return self.get_history(
            request=request,
            entity=entity,
            object_id=object_id,
            include_create=True,
        )