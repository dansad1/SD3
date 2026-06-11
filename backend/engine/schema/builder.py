from django.core.exceptions import (
    PermissionDenied,
)


class EntitySchemaBuilder:

    def __init__(self, entity):

        self.entity = entity
        self.model = entity.model

    # =====================================================
    # BUILD
    # =====================================================

    def build(
        self,
        request,
        action="view",
    ):

        # =================================================
        # ACTION VALIDATION
        # =================================================

        if action not in (
            "view",
            "create",
            "edit",
        ):

            raise PermissionDenied

        # =================================================
        # PERMISSION
        # =================================================

        self.entity.check_permission(
            request,
            action,
        )

        # =================================================
        # RUNTIME FIELDS
        # =================================================

        fields = (
            self.entity.get_fields(
                request
            )
            or []
        )

        # =================================================
        # BUILD
        # =================================================

        fields_schema = []

        seen = set()

        for field in fields:

            if not field.name:
                continue

            if field.name in seen:
                continue

            seen.add(
                field.name
            )

            schema = field.get_schema()

            if action == "view":
                schema["readonly"] = True

            fields_schema.append(
                schema
            )

        # =================================================
        # RESPONSE
        # =================================================

        return {

            "entity":
                self.entity.entity,

            "model":
                self.model.__name__,

            "fields":
                fields_schema,

            "capabilities":
                (
                    self.entity
                    .get_capabilities_for_user(
                        request
                    )
                ),
        }