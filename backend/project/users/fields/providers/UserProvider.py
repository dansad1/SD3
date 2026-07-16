import logging

from django.core.exceptions import (
    ValidationError,
)

from backend.engine.fields.providers.BaseRelationProvider import (
    BaseRelationProvider,
)
from backend.engine.fields.providers.registry import (
    register_relation_provider,
)
from backend.project.tickets.services import TicketAssignmentPolicy
from backend.project.tickets.services.TicketAssignmentPolicy import TicketAssignmentService

from backend.project.users.models import (
    User,
)


logger = logging.getLogger(__name__)


@register_relation_provider
class UserProvider(
    BaseRelationProvider,
):

    code = "user"

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_options(
        self,
        field,
        request=None,
        instance=None,
    ):

        logger.warning("=" * 80)
        logger.warning("UserProvider.get_options")
        logger.warning("field=%s", field.name)
        logger.warning("request=%s", request)

        if request:

            logger.warning(
                "user=%s",
                getattr(
                    request,
                    "user",
                    None,
                ),
            )

        if (
            field.name == "executors"
            and request
        ):

            logger.warning(
                "Using TicketAssignmentPolicy",
            )

            queryset = (
                TicketAssignmentService
                .get_allowed_executors(
                    request.user,
                )
            )

        else:

            logger.warning(
                "Using default queryset",
            )

            queryset = (
                User.objects
                .filter(
                    is_active=True,
                )
            )

        logger.warning(
            "SQL=%s",
            queryset.query,
        )

        logger.warning(
            "COUNT=%s",
            queryset.count(),
        )

        logger.warning(
            "IDS=%s",
            list(
                queryset.values_list(
                    "pk",
                    flat=True,
                )
            ),
        )

        options = [

            {
                "value": obj.pk,
                "label": str(obj),
            }

            for obj in queryset

        ]

        logger.warning(
            "OPTIONS=%s",
            options,
        )

        logger.warning("=" * 80)

        return options

    # =====================================================
    # INITIAL
    # =====================================================

    def get_initial(
        self,
        field,
        request=None,
        instance=None,
    ):

        logger.warning(
            "UserProvider.get_initial field=%s",
            field.name,
        )

        if not request:
            return None

        if not request.user.is_authenticated:
            return None

        if field.name != "requester":
            return None

        logger.warning(
            "Initial requester=%s",
            request.user,
        )

        return request.user

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        field,
        value,
        request=None,
        instance=None,
    ):

        logger.warning("=" * 80)
        logger.warning("UserProvider.validate")
        logger.warning("field=%s", field.name)
        logger.warning("value=%s", value)

        if (
            field.name == "executors"
            and value
            and request
        ):

            values = (
                value
                if isinstance(
                    value,
                    list,
                )
                else [value]
            )

            logger.warning(
                "VALUES=%s",
                values,
            )

            users = []

            for item in values:

                pk = (
                    item.get("value")
                    if isinstance(
                        item,
                        dict,
                    )
                    else item
                )

                logger.warning(
                    "Loading user %s",
                    pk,
                )

                user = (
                    User.objects
                    .filter(
                        pk=pk,
                    )
                    .first()
                )

                logger.warning(
                    "Loaded=%s",
                    user,
                )

                if not user:

                    raise ValidationError(
                        "Пользователь не найден."
                    )

                users.append(
                    user,
                )

            logger.warning(
                "Users=%s",
                users,
            )

            TicketAssignmentService.validate_executors(
                actor=request.user,
                executors=users,
            )

        logger.warning("=" * 80)

        return super().validate(
            field,
            value,
            request=request,
            instance=instance,
        )

    # =====================================================
    # NORMALIZATION
    # =====================================================

    def normalize(
        self,
        field,
        value,
        request=None,
        instance=None,
    ):

        logger.warning(
            "UserProvider.normalize %s",
            field.name,
        )

        return super().normalize(
            field,
            value,
            request=request,
            instance=instance,
        )

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def serialize(
        self,
        field,
        value,
        request=None,
        instance=None,
    ):

        logger.warning(
            "UserProvider.serialize %s",
            field.name,
        )

        return super().serialize(
            field,
            value,
            request=request,
            instance=instance,
        )

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        field,
        value,
    ):

        logger.warning(
            "UserProvider.apply_filter field=%s value=%s",
            field.name,
            value,
        )

        return super().apply_filter(
            queryset,
            field,
            value,
        )

    # =====================================================
    # BEFORE SAVE
    # =====================================================

    def before_save(
        self,
        instance,
        field,
        value,
    ):

        logger.warning(
            "UserProvider.before_save %s",
            field.name,
        )

    # =====================================================
    # AFTER SAVE
    # =====================================================

    def after_save(
        self,
        instance,
        field,
        value,
    ):

        logger.warning(
            "UserProvider.after_save %s",
            field.name,
        )