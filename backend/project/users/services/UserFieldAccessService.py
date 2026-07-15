from backend.project.users.models import (
    UserFieldAccess,
)


class UserFieldAccessService:

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

        access_map = getattr(
            request,
            cls.CACHE_NAME,
            None,
        )

        if access_map is not None:
            return access_map

        access_map = {

            access.field.name:
                access.access_level

            for access in (

                UserFieldAccess.objects

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