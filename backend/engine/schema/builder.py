import inspect

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

    # =====================================================
    # BUILD
    # =====================================================

    def build(
        self,
        request,
        action="view",
        fields=None,
        obj=None,
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

        if fields is None:

            fields = (

                self.entity.get_fields(
                    request=request,
                    obj=obj,
                )

                or []

            )

        fields_schema = []

        seen = set()

        for field in fields:

            name = getattr(
                field,
                "name",
                None,
            )

            if not name:
                continue

            if name in seen:
                continue

            seen.add(
                name,
            )

            # =================================================
            # FIELD SCHEMA
            # =================================================

            try:

                schema = field.get_schema(
                    request=request,
                    instance=obj,
                )

            except TypeError:

                #
                # Backward compatibility
                #

                schema = field.get_schema()

            # =================================================
            # RELATION OPTIONS
            # =================================================

            entity_name = schema.get(
                "entity",
            )

            if (
                entity_name
                and "options" not in schema
            ):

                try:

                    relation_entity = (
                        entity_registry.get(
                            entity_name,
                        )
                    )

                    if relation_entity:

                        schema["options"] = [

                            relation_entity.represent_option(
                                item,
                            )

                            for item in (

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
                        name,
                        entity_name,
                        exc,
                    )

                    schema["options"] = []

            # =================================================
            # ENTITY CUSTOMIZATION
            # =================================================

            method = (
                self.entity.customize_field_schema
            )

            parameters = inspect.signature(
                method,
            ).parameters

            if "obj" in parameters:

                schema = method(
                    request=request,
                    schema=schema,
                    field=field,
                    obj=obj,
                )

            else:

                #
                # Backward compatibility
                #

                schema = method(
                    request=request,
                    schema=schema,
                    field=field,
                )

            # =================================================
            # FIELD ACCESS
            # =================================================

            if getattr(
                field,
                "access_level",
                None,
            ) == "view":

                schema["readonly"] = True

            # =================================================
            # VIEW MODE
            # =================================================

            if action == "view":

                schema["readonly"] = True

            fields_schema.append(
                schema,
            )

        # =====================================================
        # RESULT
        # =====================================================

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