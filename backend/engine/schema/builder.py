from django.core.exceptions import (
    PermissionDenied,
)

from backend.engine.entity.EntityRegistry import (
    entity_registry,
)


class EntitySchemaBuilder:

    def __init__(
        self,
        entity,
    ):
        self.entity = entity
        self.model = entity.model

    def build(
        self,
        request,
        fields,
        action="view",
    ):

        if action not in (
            "view",
            "create",
            "edit",
        ):
            raise PermissionDenied

        self.entity.check_permission(
            request,
            action,
        )

        fields_schema = []

        seen = set()

        for field in fields or []:

            if not field.name:
                continue

            if field.name in seen:
                continue

            seen.add(field.name)

            schema = field.get_schema()

            # =========================================
            # RELATION OPTIONS
            # =========================================

            entity_name = schema.get(
                "entity",
            )

            if entity_name:

                try:

                    relation_entity = (
                        entity_registry.get(
                            entity_name,
                        )
                    )

                    if relation_entity:

                        schema["options"] = [

                            relation_entity.represent_option(
                                obj,
                            )

                            for obj in (
                                relation_entity.get_queryset(
                                    request,
                                )
                            )

                        ]

                    else:

                        schema["options"] = []

                except Exception as exc:

                    print(
                        "[OPTIONS ERROR]",
                        field.name,
                        entity_name,
                        exc,
                    )

                    schema["options"] = []

            schema = (
                self.entity.customize_field_schema(
                    request=request,
                    schema=schema,
                    field=field,
                )
            )

            if action == "view":
                schema["readonly"] = True

            fields_schema.append(
                schema,
            )

        return {

            "entity":
                self.entity.entity,

            "model":
                self.model.__name__,

            "fields":
                fields_schema,

            "capabilities":
                self.entity.get_capabilities_for_user(
                    request,
                ),

        }