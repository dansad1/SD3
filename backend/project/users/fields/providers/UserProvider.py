from django.core.exceptions import ValidationError

from backend.engine.fields.providers.BaseRelationProvider import (
    BaseRelationProvider,
)

from backend.engine.fields.providers.registry import (
    register_relation_provider,
)

from backend.project.tickets.services.TicketAssignmentPolicy import (
    TicketAssignmentPolicy,
)

from backend.project.users.models import (
    User,
)


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

        if (
            field.name == "executors"
            and request
        ):

            queryset = (
                TicketAssignmentPolicy
                .get_allowed_executors(
                    request.user,
                )
            )

        else:

            queryset = (
                User.objects
                .all()
            )

        options = [

            {
                "value": obj.pk,
                "label": str(obj),
            }

            for obj in queryset

        ]

        options.sort(

            key=lambda item: (
                item["label"]
                or ""
            ).casefold()

        )

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

        if not request:
            return None

        if not request.user.is_authenticated:
            return None

        if field.name != "requester":
            return None

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

        if (
            field.name == "executors"
            and value
            and request
        ):

            # если поле множественное
            values = (
                value
                if isinstance(
                    value,
                    list,
                )
                else [value]
            )

            allowed = set(
                TicketAssignmentPolicy
                .get_allowed_executors(
                    request.user,
                )
                .values_list(
                    "pk",
                    flat=True,
                )
            )

            for item in values:

                pk = (
                    item.get("value")
                    if isinstance(
                        item,
                        dict,
                    )
                    else item
                )

                if pk not in allowed:

                    raise ValidationError(
                        "Недопустимый исполнитель."
                    )

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

        pass

    # =====================================================
    # AFTER SAVE
    # =====================================================

    def after_save(
        self,
        instance,
        field,
        value,
    ):

        pass