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
        # RESULT
        # =================================================

        fields_schema = []

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
        # DEDUPLICATION
        # =================================================

        seen = set()

        # =================================================
        # BUILD
        # =================================================

        for field in fields:

            if not field.name:
                continue

            if field.name in seen:
                continue

            seen.add(field.name)

            if field.hidden:
                continue

            schema = field.get_schema()

            # =============================================
            # DEBUG
            # =============================================


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