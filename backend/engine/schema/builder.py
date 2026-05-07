from django.core.exceptions import PermissionDenied
from django.db import models

from backend.engine.schema.base import step_base
from backend.engine.schema.choices import step_choices
from backend.engine.schema.context import FieldContext
from backend.engine.schema.entity import step_entity
from backend.engine.schema.filters import (
    should_include,
    should_include_dynamic,
)
from backend.engine.schema.json import step_json
from backend.engine.schema.relations import step_relations
from backend.engine.schema.types import step_detect_type
from backend.engine.schema.widgets import step_widget


PIPELINE = [
    step_detect_type,
    step_base,
    step_widget,
    step_choices,
    step_relations,
    step_json,
    step_entity,
]


class EntitySchemaBuilder:

    def __init__(self, entity):
        self.entity = entity
        self.model = entity.model

    def build(self, request, action="view"):

        # =========================
        # ACTION VALIDATION
        # =========================

        if action not in ("view", "create", "edit"):
            raise PermissionDenied

        # =========================
        # PERMISSION
        # =========================

        self.entity.check_permission(request, action)

        # =========================
        # RESULT
        # =========================

        fields_schema = []

        # =========================
        # COLLECT FIELDS
        # =========================

        django_fields = list(
            self.model._meta.get_fields()
        )

        dynamic_fields = list(
            self.entity.get_dynamic_fields(request) or []
        )

        fields = django_fields + dynamic_fields

        # защита от дублей
        seen = set()

        # =========================
        # BUILD
        # =========================

        for field in fields:

            name = getattr(field, "name", None)

            if not name:
                continue

            if name in seen:
                continue

            seen.add(name)

            # =========================
            # DJANGO FIELD FILTER
            # =========================

            if isinstance(field, models.Field):

                if not should_include(field, self.entity):
                    continue

            # =========================
            # DYNAMIC FIELD FILTER
            # =========================

            else:

                if not should_include_dynamic(
                    field,
                    self.entity,
                    request
                ):
                    continue

            # =========================
            # CONTEXT
            # =========================

            ctx = FieldContext(
                model=self.model,
                field=field,
                entity=self.entity,
                request=request,
                action=action,
            )

            # =========================
            # PIPELINE
            # =========================

            for step in PIPELINE:
                step(ctx)

            # =========================
            # VIEW MODE
            # =========================

            if action == "view":
                ctx.schema["readonly"] = True

            # =========================
            # DEBUG
            # =========================

            print(
                "[FIELD]",
                ctx.name,
                "type=",
                ctx.type,
                "widget=",
                ctx.schema.get("widget"),
                "dynamic=",
                not isinstance(field, models.Field),
            )

            # =========================
            # RESULT
            # =========================

            fields_schema.append(ctx.schema)

        # =========================
        # RESPONSE
        # =========================

        return {
            "entity": self.entity.entity,
            "model": self.model.__name__,
            "fields": fields_schema,
            "capabilities": self.entity.get_capabilities_for_user(
                request
            ),
        }