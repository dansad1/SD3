from django.core.exceptions import (
    PermissionDenied,
)
from django.db.models import (
    Q,
)


class TicketScopeService:

    # =====================================================
    # LEVELS
    # =====================================================

    LEVEL_NONE = "none"
    LEVEL_OWN = "own"
    LEVEL_COMPANY = "company"
    LEVEL_REGION = "region"
    LEVEL_ALL = "all"

    LEVELS = (
        LEVEL_ALL,
        LEVEL_REGION,
        LEVEL_COMPANY,
        LEVEL_OWN,
    )

    # =====================================================
    # ACTIONS
    # =====================================================

    ACTION_MAP = {
        "list": "view",
        "view": "view",
        "create": "create",
        "edit": "edit",
        "delete": "delete",
    }

    # =====================================================
    # NORMALIZATION
    # =====================================================

    @classmethod
    def normalize_action(
        cls,
        action,
    ):
        return cls.ACTION_MAP.get(
            action,
        )

    # =====================================================
    # PERMISSIONS
    # =====================================================

    @classmethod
    def get_base_permission(
        cls,
        *,
        entity,
        action,
    ):
        normalized_action = cls.normalize_action(
            action,
        )

        if normalized_action is None:
            return None

        capabilities = getattr(
            entity,
            "capabilities",
            {},
        ) or {}

        if action == "list":
            return (
                capabilities.get(
                    "list",
                )
                or capabilities.get(
                    "view",
                )
            )

        return capabilities.get(
            normalized_action,
        )

    @classmethod
    def build_scope_permission(
        cls,
        *,
        entity,
        action,
        level,
    ):
        base_permission = cls.get_base_permission(
            entity=entity,
            action=action,
        )

        if not base_permission:
            return None

        return f"{base_permission}_{level}"

    @classmethod
    def get_scope_level(
        cls,
        *,
        entity,
        user,
        action,
    ):
        if (
            user is None
            or not user.is_authenticated
        ):
            return cls.LEVEL_NONE

        if user.is_superuser:
            return cls.LEVEL_ALL

        if cls.normalize_action(
            action,
        ) is None:
            return cls.LEVEL_NONE

        for level in cls.LEVELS:
            permission = cls.build_scope_permission(
                entity=entity,
                action=action,
                level=level,
            )

            if (
                permission
                and user.has_perm(
                    permission,
                )
            ):
                return level

        return cls.LEVEL_NONE

    @classmethod
    def has_scope(
        cls,
        *,
        entity,
        user,
        action,
    ):
        return (
            cls.get_scope_level(
                entity=entity,
                user=user,
                action=action,
            )
            != cls.LEVEL_NONE
        )

    @classmethod
    def check_scope(
        cls,
        *,
        entity,
        user,
        action,
    ):
        if cls.has_scope(
            entity=entity,
            user=user,
            action=action,
        ):
            return

        raise PermissionDenied(
            "Для действия не задан допустимый уровень доступа.",
        )

    # =====================================================
    # QUERYSET
    # =====================================================

    @classmethod
    def apply_queryset_scope(
        cls,
        *,
        entity,
        queryset,
        user,
        action,
    ):
        level = cls.get_scope_level(
            entity=entity,
            user=user,
            action=action,
        )

        if level == cls.LEVEL_ALL:
            return queryset

        if level == cls.LEVEL_REGION:
            return cls.filter_region(
                queryset=queryset,
                user=user,
            )

        if level == cls.LEVEL_COMPANY:
            return cls.filter_company(
                queryset=queryset,
                user=user,
            )

        if level == cls.LEVEL_OWN:
            return cls.filter_own(
                queryset=queryset,
                user=user,
                action=action,
            )

        return queryset.none()

    # =====================================================
    # OWN
    # =====================================================

    @classmethod
    def filter_own(
        cls,
        *,
        queryset,
        user,
        action,
    ):
        """
        Значение own зависит от действия.

        Просмотр:
        - создано пользователем;
        - пользователь является заявителем;
        - пользователь назначен исполнителем.

        Редактирование:
        - создано пользователем;
        - пользователь назначен исполнителем.

        Удаление:
        - только создано пользователем.
        """

        normalized_action = cls.normalize_action(
            action,
        )

        if normalized_action == "view":
            return queryset.filter(
                Q(
                    created_by_id=user.pk,
                )
                | Q(
                    requester_id=user.pk,
                )
                | Q(
                    assigned_to_id=user.pk,
                )
            ).distinct()

        if normalized_action == "edit":
            return queryset.filter(
                Q(
                    created_by_id=user.pk,
                )
                | Q(
                    assigned_to_id=user.pk,
                )
            ).distinct()

        if normalized_action == "delete":
            return queryset.filter(
                created_by_id=user.pk,
            )

        return queryset.none()

    # =====================================================
    # COMPANY
    # =====================================================

    @classmethod
    def filter_company(
        cls,
        *,
        queryset,
        user,
    ):
        company_id = getattr(
            user,
            "company_id",
            None,
        )

        if company_id is None:
            return queryset.none()

        return queryset.filter(
            company_id=company_id,
        )

    # =====================================================
    # REGION
    # =====================================================

    @classmethod
    def filter_region(
        cls,
        *,
        queryset,
        user,
    ):
        region_id = getattr(
            user,
            "region_id",
            None,
        )

        if region_id is None:
            return queryset.none()

        return queryset.filter(
            company__region_id=region_id,
        )

    # =====================================================
    # OBJECT
    # =====================================================

    @classmethod
    def can_access_object(
        cls,
        *,
        entity,
        user,
        ticket,
        action,
    ):
        if ticket is None:
            return False

        queryset = (
            entity.model.objects
            .filter(
                pk=ticket.pk,
            )
        )

        return (
            cls.apply_queryset_scope(
                entity=entity,
                queryset=queryset,
                user=user,
                action=action,
            )
            .exists()
        )

    @classmethod
    def check_object_access(
        cls,
        *,
        entity,
        user,
        ticket,
        action,
    ):
        if cls.can_access_object(
            entity=entity,
            user=user,
            ticket=ticket,
            action=action,
        ):
            return

        raise PermissionDenied(
            "Действие с этой заявкой запрещено.",
        )

    # =====================================================
    # CREATE
    # =====================================================

    @classmethod
    def validate_create(
        cls,
        *,
        entity,
        user,
        payload,
    ):
        level = cls.get_scope_level(
            entity=entity,
            user=user,
            action="create",
        )

        if level == cls.LEVEL_ALL:
            return

        if level == cls.LEVEL_REGION:
            cls.validate_create_region(
                user=user,
                payload=payload,
            )
            return

        if level == cls.LEVEL_COMPANY:
            cls.validate_create_company(
                user=user,
                payload=payload,
            )
            return

        if level == cls.LEVEL_OWN:
            cls.validate_create_own(
                user=user,
                payload=payload,
            )
            return

        raise PermissionDenied(
            "Создание заявок запрещено.",
        )

    @classmethod
    def validate_create_own(
        cls,
        *,
        user,
        payload,
    ):
        requester = payload.get(
            "requester",
        )

        requester_id = cls.get_object_id(
            requester,
        )

        if (
            requester_id is not None
            and requester_id != user.pk
        ):
            raise PermissionDenied(
                "Можно создать заявку только от своего имени.",
            )

        company = payload.get(
            "company",
        )

        company_id = cls.get_object_id(
            company,
        )

        user_company_id = getattr(
            user,
            "company_id",
            None,
        )

        if (
            company_id is not None
            and company_id != user_company_id
        ):
            raise PermissionDenied(
                "Можно создать заявку только для своей компании.",
            )

    @classmethod
    def validate_create_company(
        cls,
        *,
        user,
        payload,
    ):
        company = payload.get(
            "company",
        )

        company_id = cls.get_object_id(
            company,
        )

        user_company_id = getattr(
            user,
            "company_id",
            None,
        )

        if user_company_id is None:
            raise PermissionDenied(
                "У пользователя не указана компания.",
            )

        if company_id != user_company_id:
            raise PermissionDenied(
                "Нельзя создать заявку для другой компании.",
            )

    @classmethod
    def validate_create_region(
        cls,
        *,
        user,
        payload,
    ):
        company = payload.get(
            "company",
        )

        if company is None:
            raise PermissionDenied(
                "Для заявки необходимо указать компанию.",
            )

        company_region_id = getattr(
            company,
            "region_id",
            None,
        )

        user_region_id = getattr(
            user,
            "region_id",
            None,
        )

        if user_region_id is None:
            raise PermissionDenied(
                "У пользователя не указан регион.",
            )

        if company_region_id != user_region_id:
            raise PermissionDenied(
                "Нельзя создать заявку за пределами своего региона.",
            )

    # =====================================================
    # HELPERS
    # =====================================================

    @classmethod
    def get_object_id(
        cls,
        value,
    ):
        if value is None:
            return None

        if hasattr(
            value,
            "pk",
        ):
            return value.pk

        if isinstance(
            value,
            dict,
        ):
            return (
                value.get(
                    "value",
                )
                or value.get(
                    "id",
                )
            )

        try:
            return int(
                value,
            )
        except (
            TypeError,
            ValueError,
        ):
            return None