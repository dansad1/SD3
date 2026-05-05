from django.core.exceptions import PermissionDenied
from django.db import models

from SD3.backend.engine.schema.context import FieldContext
from SD3.backend.engine.schema.filters import should_include


class EntitySchemaBuilder:

    def __init__(self, entity):
        self.entity = entity
        self.model = entity.model

    def build(self, request, action="view"):

        if action not in ("view", "create", "edit"):
            raise PermissionDenied

        self.entity.check_permission(request, action)

        fields_schema = []

        django_fields = list(self.model._meta.get_fields())
        dynamic_fields = list(self.entity.get_dynamic_fields(request) or [])

        fields = django_fields + dynamic_fields

        seen = set()

        for field in fields:

            name = getattr(field, "name", None)

            if not name or name in seen:
                continue

            seen.add(name)

            # Django filter
            if isinstance(field, models.Field):
                if not should_include(field, self.entity):
                    continue

            # Dynamic filter
            else:
                if not self.entity.should_include_dynamic_field(request, field):
                    continue

            ctx = FieldContext(
                model=self.model,
                field=field,
                entity=self.entity,
                request=request,
                action=action,
            )

            for step in PIPELINE:
                step(ctx)

            print(
                "[FIELD]",
                ctx.name,
                "type=",
                ctx.type,
                "widget=",
                ctx.schema.get("widget"),
            )

            fields_schema.append(ctx.schema)

        return {
            "entity": self.entity.entity,
            "model": self.model.__name__,
            "fields": fields_schema,
            "capabilities": self.entity.get_capabilities_for_user(request),
        }