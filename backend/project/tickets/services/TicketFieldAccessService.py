from backend.project.tickets.models import (
    TicketFieldAccess,
)


class TicketFieldAccessService:
    CACHE_NAME = "_user_field_access_map"

    @classmethod
    def get_access_map(
            cls,
            request,
    ):

        user = request.user

        if (
                not user.is_authenticated
                or user.is_superuser
        ):
            return {}

        role = getattr(
            user,
            "role",
            None,
        )

        if role is None:
            return {}

        cached = getattr(
            request,
            cls.CACHE_NAME,
            None,
        )

        if cached is not None:
            return cached

        access_map = {

            access.field.name:
                access.access_level

            for access in (

                TicketFieldAccess.objects

                .select_related(
                    "field",
                )

                .filter(
                    role=role,
                )

            )

        }

        setattr(
            request,
            cls.CACHE_NAME,
            access_map,
        )

        return access_map
