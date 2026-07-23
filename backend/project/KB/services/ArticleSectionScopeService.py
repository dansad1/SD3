from django.db.models import Q


class ArticleSectionScopeService:

    @classmethod
    def apply(
        cls,
        request,
        queryset,
    ):
        user = request.user

        if not user.is_authenticated:
            return queryset.none()

        if user.is_superuser:
            return queryset

        role_ids = user.roles.values_list(
            "id",
            flat=True,
        )

        return (
            queryset
            .filter(
                Q(
                    user_roles__isnull=True,
                )
                | Q(
                    user_roles__id__in=role_ids,
                )
            )
            .distinct()
        )